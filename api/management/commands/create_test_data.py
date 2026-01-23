from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from typing import Dict, Any, List
import random

from api.models import AuctionItem, Bid, Question, Reply

class Command(BaseCommand):
    help = 'Create comprehensive test data for the auction site'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        self.stdout.write("🚀 Creating comprehensive test data...")
        
        # Create test users
        users = self.create_test_users()
        self.stdout.write(f"✅ Created {len(users)} test users")
        
        # Create diverse auction items
        auctions = self.create_test_auctions(users)
        self.stdout.write(f"✅ Created {len(auctions)} auction items")
        
        # Place bids on auctions
        bids = self.create_test_bids(users, auctions)
        self.stdout.write(f"✅ Created {len(bids)} bids")
        
        # Add Q&A content
        questions = self.create_test_questions(users, auctions)
        self.stdout.write(f"✅ Created {len(questions)} questions")
        
        # Add replies
        replies = self.create_test_replies(users, questions)
        self.stdout.write(f"✅ Created {len(replies)} replies")
        
        self.stdout.write(
            self.style.SUCCESS(
                "🎉 Test data creation complete!\n"
                "📊 Summary:\n"
                f"   👥 Users: {len(users)}\n"
                f"   🏷️  Auctions: {len(auctions)}\n"
                f"   💰 Bids: {len(bids)}\n"
                f"   ❓ Questions: {len(questions)}\n"
                f"   💬 Replies: {len(replies)}"
            )
        )

    def create_test_users(self) -> List[User]:
        """Create test users with specified names"""
        users_data = [
            {
                'username': 'milad.elaydi@example.com',
                'email': 'milad.elaydi@example.com',
                'first_name': 'Milad',
                'last_name': 'Elaydi',
                'password': 'testpass123',
                'date_of_birth': '1990-05-15'
            },
            {
                'username': 'hadeel.omar@example.com',
                'email': 'hadeel.omar@example.com',
                'first_name': 'Hadeel',
                'last_name': 'Omar',
                'password': 'testpass123',
                'date_of_birth': '1992-08-22'
            },
            {
                'username': 'omar.algazlan@example.com',
                'email': 'omar.algazlan@example.com',
                'first_name': 'Omar',
                'last_name': 'Algazlan',
                'password': 'testpass123',
                'date_of_birth': '1988-12-03'
            },
            {
                'username': 'sarah.jones@example.com',
                'email': 'sarah.jones@example.com',
                'first_name': 'Sarah',
                'last_name': 'Jones',
                'password': 'testpass123',
                'date_of_birth': '1995-03-17'
            },
            {
                'username': 'alex.brown@example.com',
                'email': 'alex.brown@example.com',
                'first_name': 'Alex',
                'last_name': 'Brown',
                'password': 'testpass123',
                'date_of_birth': '1987-07-09'
            }
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
            users.append(user)
        
        return users

    def create_test_auctions(self, users: List[User]) -> List[AuctionItem]:
        """Create diverse auction items with internet images"""
        auction_data = [
            {
                'title': 'Vintage Leica M3 Camera',
                'description': 'Classic 1954 Leica M3 rangefinder camera in excellent condition. Fully functional with original leather case. A collector\'s dream for photography enthusiasts.',
                'starting_price': Decimal('2500.00'),
                'category': 'electronics',
                'owner': users[0],
                'days_ahead': 7,
                'image_url': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&h=600&fit=crop'
            },
            {
                'title': 'Designer Leather Handbag',
                'description': 'Authentic designer leather handbag, barely used. Comes with dust bag and authenticity card. Perfect for special occasions.',
                'starting_price': Decimal('450.00'),
                'category': 'fashion',
                'owner': users[1],
                'days_ahead': 5,
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=600&fit=crop'
            },
            {
                'title': 'Mid-Century Modern Coffee Table',
                'description': 'Beautiful teak wood coffee table from the 1960s. Minimalist design with tapered legs. Some minor wear consistent with age.',
                'starting_price': Decimal('350.00'),
                'category': 'home',
                'owner': users[2],
                'days_ahead': 10,
                'image_url': 'https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=800&h=600&fit=crop'
            },
            {
                'title': 'Professional Tennis Racket Set',
                'description': 'Set of 2 professional-grade tennis rackets with carrying bag. Used by former college player. Great condition.',
                'starting_price': Decimal('180.00'),
                'category': 'sports',
                'owner': users[3],
                'days_ahead': 3,
                'image_url': 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&h=600&fit=crop'
            },
            {
                'title': 'Abstract Oil Painting',
                'description': 'Original abstract oil painting on canvas, 24x36 inches. Signed by emerging artist. Vibrant colors and textures.',
                'starting_price': Decimal('800.00'),
                'category': 'art',
                'owner': users[4],
                'days_ahead': 14,
                'image_url': 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=800&h=600&fit=crop'
            },
            {
                'title': 'Classic Motorcycle Parts',
                'description': 'Collection of vintage motorcycle parts for 1970s Honda CB750. Includes engine components, exhaust system, and more.',
                'starting_price': Decimal('550.00'),
                'category': 'vehicles',
                'owner': users[0],
                'days_ahead': 8,
                'image_url': 'https://images.unsplash.com/photo-1558981285-6f0c94958bb6?w=800&h=600&fit=crop'
            },
            {
                'title': 'Wireless Noise-Cancelling Headphones',
                'description': 'Premium wireless headphones with active noise cancellation. Excellent sound quality, 30-hour battery life. Like new condition.',
                'starting_price': Decimal('200.00'),
                'category': 'electronics',
                'owner': users[1],
                'days_ahead': 4,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop'
            },
            {
                'title': 'Vintage Vinyl Record Collection',
                'description': 'Collection of 50+ classic rock vinyl records from the 70s and 80s. Includes Beatles, Led Zeppelin, Pink Floyd. Well maintained.',
                'starting_price': Decimal('300.00'),
                'category': 'electronics',
                'owner': users[2],
                'days_ahead': 12,
                'image_url': 'https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800&h=600&fit=crop'
            },
            {
                'title': 'Designer Sunglasses Collection',
                'description': 'Collection of 5 designer sunglasses including Ray-Ban, Oakley, and Gucci. All authentic with cases.',
                'starting_price': Decimal('150.00'),
                'category': 'fashion',
                'owner': users[3],
                'days_ahead': 6,
                'image_url': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=800&h=600&fit=crop'
            },
            {
                'title': 'Antique Pocket Watch',
                'description': '19th century gold-plated pocket watch with chain. Still keeps time accurately. Beautiful engravings on case back.',
                'starting_price': Decimal('600.00'),
                'category': 'art',
                'owner': users[4],
                'days_ahead': 9,
                'image_url': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&h=600&fit=crop'
            }
        ]
        
        auctions = []
        for data in auction_data:
            end_time = timezone.now() + timedelta(days=data['days_ahead'])
            
            auction = AuctionItem.objects.create(
                title=data['title'],
                description=data['description'],
                starting_price=data['starting_price'],
                current_price=data['starting_price'],
                ends_at=end_time,
                category=data['category'],
                owner=data['owner'],
                image_url=data.get('image_url', '')
            )
            auctions.append(auction)
        
        return auctions

    def create_test_bids(self, users: List[User], auctions: List[AuctionItem]) -> List[Bid]:
        """Create realistic bidding activity"""
        bids = []
        
        for auction in auctions:
            # Create 2-5 bids per auction
            num_bids = random.randint(2, 5)
            bidders = [u for u in users if u != auction.owner]
            random.shuffle(bidders)
            
            current_price = float(auction.starting_price)
            
            for i in range(min(num_bids, len(bidders))):
                # Increment bid by 5-15% of current price
                increment = current_price * random.uniform(0.05, 0.15)
                new_bid_amount = round(current_price + increment, 2)
                
                bid = Bid.objects.create(
                    user=bidders[i],
                    item=auction,
                    bid_amount=Decimal(str(new_bid_amount)),
                    is_winning=(i == num_bids - 1)
                )
                bids.append(bid)
                current_price = new_bid_amount
            
            # Update auction's current price
            auction.current_price = Decimal(str(current_price))
            auction.save()
        
        return bids

    def create_test_questions(self, users: List[User], auctions: List[AuctionItem]) -> List[Question]:
        """Create realistic questions about auctions"""
        questions = []
        
        question_templates = [
            "Is this item still available for viewing before the auction ends?",
            "Would you consider shipping internationally?",
            "Are there any scratches or damage I should be aware of?",
            "What's the history of ownership for this item?",
            "Can you provide more detailed photos of specific areas?",
            "Is the original packaging included?",
            "How old is this item approximately?",
            "Are you open to best offers if the auction doesn't meet reserve?",
            "What payment methods do you accept?",
            "Is there a return policy if the item isn't as described?"
        ]
        
        for auction in auctions[:7]:  # Add questions to first 7 auctions
            num_questions = random.randint(1, 3)
            potential_questioners = [u for u in users if u != auction.owner]
            random.shuffle(potential_questioners)
            
            for i in range(min(num_questions, len(potential_questioners))):
                question_text = random.choice(question_templates)
                
                question = Question.objects.create(
                    user=potential_questioners[i],
                    item=auction,
                    question_text=question_text
                )
                questions.append(question)
        
        return questions

    def create_test_replies(self, users: List[User], questions: List[Question]) -> List[Reply]:
        """Create replies to questions"""
        replies = []
        
        reply_templates = [
            "Yes, the item is available for viewing. Please contact me to arrange a time.",
            "I can ship internationally, but the buyer would need to cover additional costs.",
            "The item is in excellent condition with no significant damage.",
            "I've owned this item for about 3 years and purchased it from an authorized dealer.",
            "I can certainly provide additional photos. Which areas would you like to see?",
            "Yes, the original packaging and all accessories are included.",
            "This item is approximately 5 years old based on the serial number.",
            "I'm open to reasonable offers after the auction ends.",
            "I accept PayPal, bank transfer, or cash on collection.",
            "I offer a 7-day return policy if the item isn't as described."
        ]
        
        for question in questions:
            # Only reply to about 70% of questions
            if random.random() < 0.7:
                reply_text = random.choice(reply_templates)
                
                reply = Reply.objects.create(
                    question=question,
                    user=question.item.owner,  # Auction owner replies
                    reply_text=reply_text
                )
                replies.append(reply)
        
        return replies
