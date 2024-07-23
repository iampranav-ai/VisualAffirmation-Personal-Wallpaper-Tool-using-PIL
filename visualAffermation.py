from PIL import Image, ImageDraw, ImageFont
import os

def create_wallpaper(text, size=(1080, 2376), bg_color="black", text_color="white", font_size=55, left_margin_percent=0.09):
    image = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(image)
    #load regular and bold fonts
    font_regular = None
    font_bold = None
    font_paths = [
        (r"C:\Windows\Fonts\LMRoman10-Regular.otf", r"C:\Windows\Fonts\LMRoman10-Bold.otf"),
        (r"C:\Users\Pranav\AppData\Local\Microsoft\Windows\Fonts\LMRoman10-Regular.otf", 
         r"C:\Users\Pranav\AppData\Local\Microsoft\Windows\Fonts\LMRoman10-Bold.otf"),
        ("LMRoman10-Regular.otf", "LMRoman10-Bold.otf"),
        ("Arial.ttf", "Arial_Bold.ttf"),
    ]
    for regular_path, bold_path in font_paths:
        try:
            font_regular = ImageFont.truetype(regular_path, font_size)
            font_bold = ImageFont.truetype(bold_path, font_size)
            font_bold_larger = ImageFont.truetype(bold_path, int(font_size * 1.2))  #new font with larger size
            print(f"Using fonts: {regular_path} and {bold_path}")
            break
        except IOError:
            continue
    if font_regular is None or font_bold is None:
        print("No suitable fonts found. Using default font.")
        font_regular = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_bold_larger = ImageFont.load_default()

    lines = text.split('\n')
    # valculate line heights and total height
    line_heights = [draw.textbbox((0, 0), lines[0], font=font_bold_larger)[3] - draw.textbbox((0, 0), lines[0], font=font_bold_larger)[1]]
    line_heights += [draw.textbbox((0, 0), line, font=font_regular)[3] - draw.textbbox((0, 0), line, font=font_regular)[1] for line in lines[1:]]
    
    gap_height = line_heights[0] // 2  # Use half the height of the first line as the gap
    total_height = sum(line_heights) + gap_height * (len(lines) - 1)
    
    #start y position (vertically centered)
    y_position = (size[1] - total_height) / 1.6
    # set left margin
    left_margin = size[0] * left_margin_percent  # Adjustable left margin
    # draw each line
    for i, line in enumerate(lines):
        if i == 0:
            # first line: bold and larger
            draw.text((left_margin, y_position), line, font=font_bold_larger, fill=text_color)
            y_position += line_heights[i] + gap_height
        else:
            # remaining lines: regular font
            draw.text((left_margin, y_position), line, font=font_regular, fill=text_color)
            y_position += line_heights[i] + gap_height
    return image

def open_image(path):
    if os.name == 'nt':
        os.startfile(path)

wallpaper_text = "Dear Pranav in 6 months,\nI am going to make you\nso damn proud."
wallpaper = create_wallpaper(wallpaper_text)

# Get the current working directory and create the full path for the image
current_dir = os.getcwd()
image_filename = "motivational_wallpaper.png"
image_path = os.path.join(current_dir, image_filename)

wallpaper.save(image_path)

print(f"Wallpaper created successfully!")
print(f"Image saved at: {image_path}")

# Automatically open the image
open_image(image_path)