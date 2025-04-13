import os
from PIL import Image
import numpy as np

def calculate_target_quality(original_size, target_size_mb=10):
    """Calculate target quality with better preservation of image quality"""
    target_size_bytes = target_size_mb * 1024 * 1024
    quality_ratio = min(1.0, target_size_bytes / original_size)
    # Start with higher base quality
    return max(60, int(quality_ratio * 98))

def compress_image(input_path, output_path, target_size_mb=10):
    """Compress an image while preserving quality"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        original_size = os.path.getsize(input_path)
        
        with Image.open(input_path) as img:
            # Preserve EXIF data if available
            try:
                exif = img.info.get('exif', None)
            except:
                exif = None
            
            # Convert RGBA to RGB with white background
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # For JPEG and WEBP
            if input_path.lower().endswith(('.jpg', '.jpeg', '.webp')):
                quality = calculate_target_quality(original_size, target_size_mb)
                
                # Try with different subsampling settings
                subsamplings = [0, 2, 1]  # 4:4:4, 4:2:0, 4:2:2
                for subsampling in subsamplings:
                    img.save(output_path, quality=quality, optimize=True, 
                           subsampling=subsampling, exif=exif)
                    current_size = os.path.getsize(output_path)
                    
                    if current_size <= (target_size_mb * 1024 * 1024):
                        break
                
                # If still too large, use binary search with best subsampling
                if current_size > (target_size_mb * 1024 * 1024):
                    low, high = 60, quality
                    while low < high - 1:
                        mid = (low + high) // 2
                        img.save(output_path, quality=mid, optimize=True,
                               subsampling=0, exif=exif)
                        current_size = os.path.getsize(output_path)
                        
                        if current_size <= (target_size_mb * 1024 * 1024):
                            low = mid
                        else:
                            high = mid
            
            # For PNG
            elif input_path.lower().endswith('.png'):
                # Try different optimization strategies
                img.save(output_path, optimize=True, quality=95)
                current_size = os.path.getsize(output_path)
                
                if current_size > (target_size_mb * 1024 * 1024):
                    # Try reducing colors while preserving quality
                    colors = 256
                    while colors >= 32 and current_size > (target_size_mb * 1024 * 1024):
                        quantized = img.quantize(colors=colors, method=2)  # Use median cut method
                        quantized.save(output_path, optimize=True)
                        current_size = os.path.getsize(output_path)
                        colors = colors // 2
                        
                    # If still too large, try converting to high-quality JPEG
                    if current_size > (target_size_mb * 1024 * 1024):
                        output_jpg = os.path.splitext(output_path)[0] + '.jpg'
                        img.save(output_jpg, 'JPEG', quality=95, optimize=True)
                        if os.path.getsize(output_jpg) < current_size:
                            os.replace(output_jpg, output_path)
            
            # For other formats
            else:
                img.save(output_path, quality=95, optimize=True)
        
        return True
        
    except Exception as e:
        raise Exception(f"Error processing {input_path}: {str(e)}")

def batch_compress(input_folder, output_folder, target_size_mb=10):
    """Compress all images in a folder"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    results = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                compress_image(input_path, output_path, target_size_mb)
                results.append({'filename': filename, 'success': True})
            except Exception as e:
                results.append({'filename': filename, 'success': False, 'error': str(e)})
    
    return results