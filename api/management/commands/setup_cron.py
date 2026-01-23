from django.core.management.base import BaseCommand
from django.conf import settings
import os
from typing import Dict, Any

class Command(BaseCommand):
    help = 'Setup cron job for automatic auction closing'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        """Setup cron job to run auction closing command every 5 minutes"""
        
        # Get the Python path and manage.py location
        python_path = os.path.join(settings.BASE_DIR, 'venv', 'bin', 'python')
        if not os.path.exists(python_path):
            python_path = 'python3'  # Fallback to system python
        
        manage_py = os.path.join(settings.BASE_DIR, 'manage.py')
        
        # Cron job command
        cron_command = f"*/5 * * * * cd {settings.BASE_DIR} && {python_path} {manage_py} close_auctions >> {settings.BASE_DIR}/logs/cron.log 2>&1"
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        self.stdout.write("🕐 Setting up cron job for automatic auction closing...")
        self.stdout.write(f"📍 Command: {cron_command}")
        self.stdout.write(f"📁 Log file: {logs_dir}/cron.log")
        
        # Instructions for manual cron setup
        self.stdout.write("\n📋 To set up the cron job manually:")
        self.stdout.write("1. Run: crontab -e")
        self.stdout.write(f"2. Add this line:")
        self.stdout.write(f"   {cron_command}")
        self.stdout.write("3. Save and exit")
        
        self.stdout.write(
            self.style.SUCCESS(
                "\n✅ Cron job setup instructions provided!\n"
                "⚡ The system will now check for ended auctions every 5 minutes\n"
                "📧 Winners will receive automatic email notifications"
            )
        )
