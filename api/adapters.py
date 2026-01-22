from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter for django-allauth account management."""
    
    def save_user(self, request, user, form, commit=True):
        """Save user with our custom fields."""
        user = super().save_user(request, user, form, commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter for social account management."""
    
    def pre_social_login(self, request, sociallogin):
        """
        Connect social account to existing user if email matches.
        """
        if sociallogin.is_existing:
            return
        
        email = sociallogin.account.extra_data.get('email')
        if email:
            from api.models import User
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
    
    def save_user(self, request, sociallogin, form=None):
        """Save user from social login with proper username."""
        user = super().save_user(request, sociallogin, form)
        user.username = user.email
        user.save()
        return user
    
    def populate_user(self, request, sociallogin, data):
        """Populate user data from social account."""
        user = super().populate_user(request, sociallogin, data)
        user.username = data.get('email', '')
        return user
