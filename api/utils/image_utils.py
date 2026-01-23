from PIL import Image, ImageOps
import os
from typing import Optional, Tuple
from django.conf import settings
import uuid

def process_uploaded_image(image, max_size: Tuple[int, int] = (800, 800), 
                          thumbnail_size: Tuple[int, int] = (200, 200)) -> dict:
    """
    Process uploaded image: resize, create thumbnail, optimize
    Returns dict with paths and metadata
    """
    try:
        # Open and process image
        img = Image.open(image)
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Auto-orient image based on EXIF data
        img = ImageOps.exif_transpose(img)
        
        # Generate unique filename
        original_filename = str(image.name)
        file_extension = original_filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Create paths
        media_root = os.path.join(settings.BASE_DIR, 'media')
        items_dir = os.path.join(media_root, 'items')
        thumbnails_dir = os.path.join(media_root, 'thumbnails')
        
        # Ensure directories exist
        os.makedirs(items_dir, exist_ok=True)
        os.makedirs(thumbnails_dir, exist_ok=True)
        
        # Save original (resized) image
        original_path = os.path.join(items_dir, unique_filename)
        img_copy = img.copy()
        img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
        img_copy.save(original_path, 'JPEG', quality=85, optimize=True)
        
        # Create and save thumbnail
        thumbnail_path = os.path.join(thumbnails_dir, unique_filename)
        thumbnail = img.copy()
        thumbnail.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        thumbnail.save(thumbnail_path, 'JPEG', quality=80, optimize=True)
        
        # Get file sizes
        original_size = os.path.getsize(original_path)
        thumbnail_size_bytes = os.path.getsize(thumbnail_path)
        
        return {
            'success': True,
            'original_filename': original_filename,
            'unique_filename': unique_filename,
            'original_path': f"items/{unique_filename}",
            'thumbnail_path': f"thumbnails/{unique_filename}",
            'original_size': original_size,
            'thumbnail_size': thumbnail_size_bytes,
            'dimensions': img.size,
            'file_size_kb': round(original_size / 1024, 2)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def create_profile_image(image, max_size: Tuple[int, int] = (400, 400)) -> dict:
    """
    Process profile image with square crop and resize
    """
    try:
        # Open and process image
        img = Image.open(image)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Auto-orient image
        img = ImageOps.exif_transpose(img)
        
        # Create square crop (centered)
        width, height = img.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        
        # Resize to max size
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Generate unique filename
        original_filename = str(image.name)
        file_extension = original_filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Create path
        media_root = os.path.join(settings.BASE_DIR, 'media')
        profile_dir = os.path.join(media_root, 'profile_images')
        os.makedirs(profile_dir, exist_ok=True)
        
        # Save image
        profile_path = os.path.join(profile_dir, unique_filename)
        img.save(profile_path, 'JPEG', quality=85, optimize=True)
        
        return {
            'success': True,
            'filename': unique_filename,
            'path': f"profile_images/{unique_filename}",
            'size': os.path.getsize(profile_path),
            'dimensions': img.size
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
