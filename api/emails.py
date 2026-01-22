from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_winner_notification(winner_email, winner_name, auction_title, winning_bid, end_date, seller_name, auction_description, auction_url):
    """
    Send winner notification email to the auction winner
    """
    try:
        subject = f'{settings.EMAIL_SUBJECT_PREFIX}Congratulations! You Won the Auction for "{auction_title}"'
        
        context = {
            'auction_title': auction_title,
            'winning_bid': winning_bid,
            'end_date': end_date,
            'seller_name': seller_name,
            'auction_description': auction_description,
            'auction_url': auction_url,
            'winner_name': winner_name,
        }
        
        # HTML template
        html_message = render_to_string('emails/winner_notification.html', context)
        
        # Plain text version (fallback)
        plain_message = f"""
Congratulations {winner_name}!

You have won the auction for "{auction_title}"!

Auction Details:
- Winning Bid: £{winning_bid}
- Auction Ended: {end_date}
- Seller: {seller_name}
{f'- Description: {auction_description}' if auction_description else ''}

View the auction details here: {auction_url}

Next Steps:
1. Contact the seller to arrange payment and delivery
2. Keep all communication records for your protection
3. Leave feedback for the seller after receiving your item

Thank you for using our auction platform!

This is an automated message. Please do not reply to this email.
© 2026 Bido. All rights reserved.
        """.strip()
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[winner_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Winner notification sent successfully to {winner_email} for auction '{auction_title}'")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send winner notification to {winner_email}: {str(e)}")
        return False

def send_outbid_notification(bidder_email, bidder_name, auction_title, current_bid, auction_url):
    """
    Send notification when user is outbid
    """
    try:
        subject = f'{settings.EMAIL_SUBJECT_PREFIX}You have been outbid on "{auction_title}"'
        
        message = f"""
Hello {bidder_name},

You have been outbid on the auction for "{auction_title}".

Current highest bid: £{current_bid}

If you still want this item, place a new bid before the auction ends!

View auction here: {auction_url}

Good luck!

This is an automated message. Please do not reply to this email.
© 2026 Bido. All rights reserved.
        """.strip()
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[bidder_email],
            fail_silently=False,
        )
        
        logger.info(f"Outbid notification sent to {bidder_email} for auction '{auction_title}'")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send outbid notification to {bidder_email}: {str(e)}")
        return False

def send_auction_ending_notification(watchers, auction_title, hours_remaining, auction_url):
    """
    Send notification to watchers when auction is ending soon
    """
    try:
        subject = f'{settings.EMAIL_SUBJECT_PREFIX}Auction Ending Soon: "{auction_title}"'
        
        message = f"""
Hello,

The auction for "{auction_title}" is ending in {hours_remaining} hours!

Don't miss your chance to bid on this item.

View auction here: {auction_url}

Place your bid before it's too late!

This is an automated message. Please do not reply to this email.
© 2026 Bido. All rights reserved.
        """.strip()
        
        # Send to all watchers
        recipient_list = [watcher.email for watcher in watchers]
        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            
            logger.info(f"Auction ending notification sent to {len(recipient_list)} watchers for '{auction_title}'")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Failed to send auction ending notification for '{auction_title}': {str(e)}")
        return False
