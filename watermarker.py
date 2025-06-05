import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# --- Configuration & Helper Functions ---

# Standard font paths
DEFAULT_FONT_PATHS = [
    "arial.ttf",  # Windows default
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Linux common
    "/System/Library/Fonts/Supplemental/Arial.ttf" # macOS
]

def find_font(font_name="arial.ttf", size=40):
    """Tries to load a font from common locations or a default."""
    for font_path_option in DEFAULT_FONT_PATHS:
        try:
            return ImageFont.truetype(font_path_option, size)
        except IOError:
            pass
    # Fallback if specific font is not found in common locations
    try:
        return ImageFont.truetype(font_name, size) # Try direct name (if in system path)
    except IOError:
        print(f"Warning: Font '{font_name}' not found. Using default system font.")
        try:
            return ImageFont.load_default() # PIL's built-in fallback
        except Exception as e:
            print(f"Error loading default font: {e}. Text watermarking might not work as expected.")
            return None


def get_user_input(prompt, default=None):
    """Gets input from the user, offering a default value."""
    if default is not None:
        response = input(f"{prompt} (default: {default}): ").strip()
        return response if response else default
    else:
        response = input(f"{prompt}: ").strip()
        while not response:
            print("Input cannot be empty.")
            response = input(f"{prompt}: ").strip()
        return response

def get_file_path(prompt, check_exists=True, is_image=True):
    """Gets a file path from the user and validates it."""
    while True:
        path = get_user_input(prompt)
        if not path:
            return None # User cancelled or entered nothing
        if check_exists and not os.path.exists(path):
            print(f"Error: File or directory '{path}' not found.")
            continue
        if check_exists and not os.path.isfile(path):
            print(f"Error: '{path}' is not a file.")
            continue
        if is_image:
            try:
                # Try to open to check if it's a valid image, but don't keep it open
                img = Image.open(path)
                img.close()
            except IOError:
                print(f"Error: '{path}' is not a valid image file or cannot be opened.")
                continue
        return os.path.abspath(path)

def get_choice(prompt, options):
    """Gets a choice from a list of options."""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        try:
            choice = int(get_user_input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_opacity():
    """Gets opacity from user (0.0 to 1.0)."""
    while True:
        try:
            opacity = float(get_user_input("Enter opacity for watermark (0.0 to 1.0, e.g., 0.5)", "0.5"))
            if 0.0 <= opacity <= 1.0:
                return opacity
            else:
                print("Opacity must be between 0.0 and 1.0.")
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 0.5).")

def calculate_position(base_width, base_height, wm_width, wm_height, position_choice, padding=10):
    """Calculates x, y coordinates for the watermark based on position choice."""
    if position_choice == "Top Left":
        return padding, padding
    elif position_choice == "Top Right":
        return base_width - wm_width - padding, padding
    elif position_choice == "Bottom Left":
        return padding, base_height - wm_height - padding
    elif position_choice == "Bottom Right":
        return base_width - wm_width - padding, base_height - wm_height - padding
    elif position_choice == "Center":
        return (base_width - wm_width) // 2, (base_height - wm_height) // 2
    # Default to bottom right if something goes wrong
    return base_width - wm_width - padding, base_height - wm_height - padding


# --- Watermarking Functions ---

def add_text_watermark(base_image_path, output_path):
    """Adds a customizable text watermark to an image."""
    print("\n--- Text Watermark ---")
    watermark_text = get_user_input("Enter watermark text:", "Sample Watermark")
    font_size = int(get_user_input("Enter font size (e.g., 50):", "50"))
    
    # Font color
    color_choices = {"White": (255, 255, 255), "Black": (0, 0, 0), "Red": (255, 0, 0), "Gray": (128, 128, 128)}
    print("Choose font color:")
    color_name = get_choice("Font color:", list(color_choices.keys()))
    font_color_rgb = color_choices[color_name]

    opacity = get_opacity()
    font_alpha = int(opacity * 255)
    font_color_rgba = font_color_rgb + (font_alpha,)

    position_options = ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center"]
    position_choice = get_choice("Choose watermark position:", position_options)
    
    font_file_path_input = get_user_input(f"Enter path to .ttf font file (leave blank for default Arial):", "")
    font = None
    if font_file_path_input and os.path.exists(font_file_path_input):
        try:
            font = ImageFont.truetype(font_file_path_input, font_size)
        except IOError:
            print(f"Could not load font from {font_file_path_input}. Trying default.")
            font = find_font(size=font_size)
    else:
        font = find_font(size=font_size)

    if not font:
        print("Error: Font not loaded. Cannot apply text watermark.")
        return False

    try:
        base_image = Image.open(base_image_path).convert("RGBA")
        
        # Create a transparent layer for the text
        txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Calculate text size (Pillow version differences)
        try:
            # For Pillow >= 9.2.0
            left, top, right, bottom = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = right - left
            text_height = bottom - top
        except AttributeError:
            # For older Pillow versions
            text_width, text_height = draw.textsize(watermark_text, font=font)


        x, y = calculate_position(base_image.width, base_image.height, text_width, text_height, position_choice)
        
        draw.text((x, y), watermark_text, font=font, fill=font_color_rgba)
        
        # Composite the text layer onto the base image
        watermarked_image = Image.alpha_composite(base_image, txt_layer)
        watermarked_image = watermarked_image.convert("RGB") # Convert back to RGB if saving as JPG
        
        watermarked_image.save(output_path)
        print(f"Text watermark applied successfully. Saved to: {output_path}")
        return True
    except Exception as e:
        print(f"Error applying text watermark: {e}")
        return False


def add_image_watermark(base_image_path, output_path):
    """Adds an image as a watermark to another image."""
    print("\n--- Image Watermark ---")
    watermark_image_path = get_file_path("Enter path to the watermark image file:", is_image=True)
    if not watermark_image_path:
        print("No watermark image selected. Aborting.")
        return False

    opacity = get_opacity()
    
    scale_factor_str = get_user_input("Enter scale factor for watermark image (e.g., 0.2 for 20% of base image width, or 1 for original size):", "0.2")
    try:
        scale_factor = float(scale_factor_str)
        if scale_factor <= 0:
            print("Scale factor must be positive. Using default 0.2.")
            scale_factor = 0.2
    except ValueError:
        print("Invalid scale factor. Using default 0.2.")
        scale_factor = 0.2

    position_options = ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center", "Tile"]
    position_choice = get_choice("Choose watermark position:", position_options)

    try:
        base_image = Image.open(base_image_path).convert("RGBA")
        watermark_image_orig = Image.open(watermark_image_path).convert("RGBA")

        # Resize watermark
        if scale_factor != 1.0: # Only scale if not 1.0
            wm_width = int(base_image.width * scale_factor) if scale_factor < 1 else int(watermark_image_orig.width * scale_factor) # if scale > 1, scale original wm
            aspect_ratio = watermark_image_orig.height / watermark_image_orig.width
            wm_height = int(wm_width * aspect_ratio)
            watermark_image = watermark_image_orig.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
        else:
            watermark_image = watermark_image_orig
            wm_width, wm_height = watermark_image.size

        # Apply opacity
        if opacity < 1.0:
            alpha = watermark_image.split()[3] # Get alpha channel
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark_image.putalpha(alpha)

        if position_choice == "Tile":
            # Create a new transparent layer matching base_image size
            watermarked_image = base_image.copy()
            for y in range(0, base_image.height, wm_height + 20): # 20px padding between tiles
                for x in range(0, base_image.width, wm_width + 20):
                    watermarked_image.alpha_composite(watermark_image, dest=(x,y))
        else:
            # Single position
            x, y = calculate_position(base_image.width, base_image.height, wm_width, wm_height, position_choice)
            
            # Create a transparent layer for the watermark to be placed on
            temp_layer = Image.new("RGBA", base_image.size, (0,0,0,0))
            temp_layer.paste(watermark_image, (x,y), watermark_image if watermark_image.mode == 'RGBA' else None)
            
            watermarked_image = Image.alpha_composite(base_image, temp_layer)

        watermarked_image = watermarked_image.convert("RGB") # Convert for saving, e.g. as JPG
        watermarked_image.save(output_path)
        print(f"Image watermark applied successfully. Saved to: {output_path}")
        return True
    except FileNotFoundError:
        print(f"Error: Watermark image '{watermark_image_path}' not found.")
        return False
    except Exception as e:
        print(f"Error applying image watermark: {e}")
        return False

# --- Main Program ---
def main():
    print("==============================================")
    print("        PYTHON IMAGE WATERMARKER           ")
    print("==============================================")
    print("This script will add a watermark to your image.")
    print("----------------------------------------------\n")

    base_image_path = get_file_path("Enter path to the base image you want to watermark:")
    if not base_image_path:
        print("No base image selected. Exiting.")
        return

    # Determine output path
    base_dir = os.path.dirname(base_image_path)
    base_filename, base_ext = os.path.splitext(os.path.basename(base_image_path))
    default_output_path = os.path.join(base_dir, f"{base_filename}_watermarked{base_ext}")
    output_path = get_user_input(f"Enter path for the watermarked output image:", default_output_path)
    if not output_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        print("Warning: Output path does not have a common image extension. Saving as PNG by default if not specified.")
        if '.' not in os.path.basename(output_path): # if no extension at all
            output_path += ".png"


    watermark_type_choice = get_choice("Choose watermark type:", ["Text", "Image"])

    success = False
    if watermark_type_choice == "Text":
        success = add_text_watermark(base_image_path, output_path)
    elif watermark_type_choice == "Image":
        success = add_image_watermark(base_image_path, output_path)

    if success:
        print(f"\nWatermarked image saved as {output_path}")
    else:
        print("\nWatermarking process failed or was aborted.")

    print("\nExiting program.")

if __name__ == "__main__":
    main()