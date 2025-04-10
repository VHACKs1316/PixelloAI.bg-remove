import sys
import cv2
import numpy as np
from rembg import remove
from PIL import Image

def process_image(input_path, output_path):
    try:
        # Read the input image
        input_image = Image.open(input_path)
        
        # Remove background
        output_image = remove(input_image)
        
        # Save the result
        output_image.save(output_path, 'PNG')
        
        return True
    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process-image.py <input_path> <output_path>", file=sys.stderr)
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    success = process_image(input_path, output_path)
    sys.exit(0 if success else 1)