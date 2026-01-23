from django.core.management.base import BaseCommand
from django.conf import settings
import os
from typing import Dict, Any

class Command(BaseCommand):
    help = 'Setup proper media storage directories and permissions'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        """Create media directories and set up proper storage"""
        
        self.stdout.write("🗂️  Setting up media storage...")
        
        # Create media directories
        media_dirs = [
            'media',
            'media/profile_images',
            'media/items',
            'media/thumbnails'
        ]
        
        for dir_path in media_dirs:
            full_path = os.path.join(settings.BASE_DIR, dir_path)
            os.makedirs(full_path, exist_ok=True)
            self.stdout.write(f"✅ Created: {dir_path}")
        
        # Create .gitkeep files to track empty directories
        gitkeep_dirs = [
            'media/profile_images/.gitkeep',
            'media/items/.gitkeep', 
            'media/thumbnails/.gitkeep'
        ]
        
        for gitkeep_path in gitkeep_dirs:
            full_path = os.path.join(settings.BASE_DIR, gitkeep_path)
            if not os.path.exists(full_path):
                with open(full_path, 'w') as f:
                    f.write('# This file ensures the directory is tracked by git\n')
                self.stdout.write(f"✅ Created: {gitkeep_path}")
        
        self.stdout.write(
            self.style.SUCCESS(
                "🎉 Media storage setup complete!\n"
                "📁 Directories created:\n"
                "   - media/profile_images/\n"
                "   - media/items/\n"
                "   - media/thumbnails/\n"
                "🔧 Ready for image uploads"
            )
        )
