from PIL import Image
import os

def convert_image(input_path: str, output_format: str):
    try:
        # Open the original image
        with Image.open(input_path) as img:
            # Remove old extension and apply new one
            base_path = os.path.splitext(input_path)[0]
            new_path = f"{base_path}.{output_format.lower()}"
            
            # Convert to RGB if saving as JPEG (JPEG doesn't support transparency/RGBA)
            if output_format.upper() in ["JPG", "JPEG"] and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            img.save(new_path, output_format.upper())
            return f"Success! Saved at: {new_path}"
    except Exception as e:
        return f"Conversion Error: {str(e)}"