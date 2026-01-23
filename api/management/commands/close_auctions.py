from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal
import logging

from api.models import AuctionItem, Bid, User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Close ended auctions and send winner notification emails'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually closing auctions or sending emails',
        )
        parser.add_argument(
            '--test-email',
            type=str,
            help='Send test email to this address instead of actual winner',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        test_email = options['test_email']
        
        self.stdout.write(
            self.style.SUCCESS(
                f"🚀 Starting auction closure process "
                f"{'(DRY RUN)' if dry_run else ''}"
            )
        )
        
        # Find auctions that have ended but are still active
        ended_auctions = AuctionItem.objects.filter(
            ends_at__lte=timezone.now(),
            status='active'
        ).select_related('owner').prefetch_related('bids__user')
        
        if not ended_auctions.exists():
            self.stdout.write(
                self.style.WARNING("No ended auctions found to process")
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f"📊 Found {ended_auctions.count()} ended auction(s) to process"
            )
        )
        
        closed_count = 0
        email_sent_count = 0
        error_count = 0
        
        for auction in ended_auctions:
            try:
                with transaction.atomic():
                    result = self.process_auction(auction, dry_run, test_email)
                    if result['closed']:
                        closed_count += 1
                    if result['email_sent']:
                        email_sent_count += 1
                    if result['error']:
                        error_count += 1
                        
            except Exception as e:
                error_count += 1
                logger.error(f"Error processing auction {auction.id}: {str(e)}")
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Error processing auction {auction.id}: {str(e)}"
                    )
                )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f"\n📈 Summary:"
                f"\n   ✅ Auctions processed: {ended_auctions.count()}"
                f"\n   🔒 Auctions closed: {closed_count}"
                f"\n   📧 Emails sent: {email_sent_count}"
                f"\n   ❌ Errors: {error_count}"
                f"\n   {'🧪 DRY RUN MODE' if dry_run else '🚀 LIVE MODE'}"
            )
        )

    def process_auction(self, auction, dry_run=False, test_email=None):
        """Process a single ended auction"""
        result = {
            'closed': False,
            'email_sent': False,
            'error': False,
            'winner': None,
            'winning_bid': None
        }
        
        # Find the highest bid
        highest_bid = auction.bids.order_by('-bid_amount', '-timestamp').first()
        
        if not highest_bid:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Auction {auction.id} ({auction.title}) ended with no bids"
                )
            )
            
            # Prepare email data for seller notification (no bids)
            email_data = {
                'auction': auction,
                'winner': None,
                'winning_bid': None,
                'winning_amount': None,
                'seller': auction.owner,
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
            }
            
            if not dry_run:
                # Send seller notification about no bids
                seller_sent = self.send_seller_notification(auction.owner.email, email_data)
                
                if seller_sent:
                    result['email_sent'] = True
                    
                    # Close the auction
                    auction.status = 'closed'
                    auction.closed_at = timezone.now()
                    auction.save()
                    result['closed'] = True
                else:
                    result['error'] = True
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"🧪 DRY RUN: Would send seller notification about no bids to {auction.owner.email}"
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        f"🧪 DRY RUN: Would close auction {auction.id} - {auction.title}"
                    )
                )
                result['closed'] = True  # Simulate closing in dry run
            
            return result
        
        # Determine winner and email recipient
        winner = highest_bid.user
        winning_amount = highest_bid.bid_amount
        
        # Prepare email data for winner (using winner's currency)
        winner_email_data = {
            'auction': auction,
            'winner': winner,
            'winning_bid': winner.format_currency(winning_amount),
            'starting_price': winner.format_currency(auction.starting_price),
            'winning_amount': winning_amount,
            'seller': auction.owner,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        # Prepare email data for seller (using seller's currency)
        seller_email_data = {
            'auction': auction,
            'winner': winner,
            'winning_bid': auction.owner.format_currency(winning_amount),
            'starting_price': auction.owner.format_currency(auction.starting_price),
            'winning_amount': winning_amount,
            'seller': auction.owner,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        # Send winner notification
        email_recipient = test_email if test_email else winner.email
        
        try:
            if not dry_run:
                # Send email to winner
                winner_sent = self.send_winner_email(email_recipient, winner_email_data)
                
                # Also notify seller
                seller_sent = self.send_seller_notification(auction.owner.email, seller_email_data)
                
                if winner_sent and seller_sent:
                    result['email_sent'] = True
                    
                    # Close the auction
                    auction.status = 'closed'
                    auction.winner = winner
                    auction.winning_bid_amount = winning_amount
                    auction.closed_at = timezone.now()
                    auction.save()
                    result['closed'] = True
                    result['winner'] = winner
                    result['winning_bid'] = highest_bid
                    
                    # Create in-app notifications
                    # Winner notification
                    from api.models import Notification
                    from api.utils import create_and_send_notification
                    create_and_send_notification(
                        winner,
                        'auction_won',
                        f'🎉 Congratulations! You won the auction for "{auction.title}" with a bid of ${winning_amount:.2f}',
                    )
                    
                    # Notify all other bidders that they lost
                    other_bidders = Bid.objects.filter(item=auction).exclude(user=winner).values_list('user', flat=True).distinct()
                    for bidder_id in other_bidders:
                        from django.contrib.auth import get_user_model
                        User = get_user_model()
                        bidder = User.objects.get(id=bidder_id)
                        create_and_send_notification(
                            bidder,
                            'auction_lost',
                            f'The auction "{auction.title}" has ended. The winning bid was ${winning_amount:.2f}',
                        )
                else:
                    result['error'] = True
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"🧪 DRY RUN: Would send winner email to {email_recipient}"
                    )
                )
                self.stdout.write(
                    self.style.WARNING(
                        f"🧪 DRY RUN: Would close auction {auction.id} - {auction.title}"
                    )
                )
                result['closed'] = True  # Simulate closing in dry run
                
        except Exception as e:
            logger.error(f"Failed to send email for auction {auction.id}: {str(e)}")
            result['error'] = True
        
        # Log the result
        if result['email_sent']:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Auction {auction.id} closed - Winner: {winner.username} "
                    f"(${winning_amount:.2f})"
                )
            )
        elif result['error']:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Failed to process auction {auction.id}"
                )
            )
        
        return result

    def send_winner_email(self, recipient_email, email_data):
        """Send winner notification email"""
        try:
            subject = f"🎉 Congratulations! You won the auction for {email_data['auction'].title}"
            
            # Create HTML email content
            html_message = render_to_string('emails/winner_notification.html', email_data)
            plain_message = render_to_string('emails/winner_notification.txt', email_data)
            
            # Send email
            sent = send_mail(
                subject=subject,
                message=plain_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@auctionsite.com'),
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            if sent:
                logger.info(f"Winner notification sent to {recipient_email}")
                return True
            else:
                logger.error(f"Failed to send winner notification to {recipient_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending winner email to {recipient_email}: {str(e)}")
            return False

    def send_seller_notification(self, seller_email, email_data):
        """Send notification to seller about auction ending"""
        try:
            subject = f"🏆 Your auction '{email_data['auction'].title}' has ended"
            
            # Create HTML email content
            html_message = render_to_string('emails/seller_notification.html', email_data)
            plain_message = render_to_string('emails/seller_notification.txt', email_data)
            
            # Send email
            sent = send_mail(
                subject=subject,
                message=plain_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@auctionsite.com'),
                recipient_list=[seller_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            if sent:
                logger.info(f"Seller notification sent to {seller_email}")
                return True
            else:
                logger.error(f"Failed to send seller notification to {seller_email}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending seller email to {seller_email}: {str(e)}")
            return False
