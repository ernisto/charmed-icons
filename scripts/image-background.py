from collections import Counter
from PIL import Image
import cairosvg
import os
import io

def add_transparent_background(image):

    datas = image.getdata()

    pixels = list(datas)
    color_counter = Counter(pixels)

    colors = color_counter.most_common(3)
    primary_color = colors[0][0] if colors[0][0][3] >= 200 else \
        colors[1][0] if colors[1][0][3] >= 200 else \
        colors[2][0]

    bg_color = (primary_color[0], primary_color[1], primary_color[2], 100)

    new_data = []
    for item in datas:
        alpha = 1 - item[3] / bg_color[3] if bg_color[3] > 0 else 0
        if alpha < 0:
            alpha = 0
        new_data.append((
            int(item[0] + (bg_color[0] - item[0]) * alpha),
            int(item[1] + (bg_color[1] - item[1]) * alpha),
            int(item[2] + (bg_color[2] - item[2]) * alpha),
            int(item[3] + (bg_color[3] - item[3]) * alpha),
        ))

    image.putdata(new_data)

def process_svgs(input_folder, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if not file_name.endswith('.svg'):
            continue

        svg_path = os.path.join(input_folder, file_name)
        png_name = os.path.splitext(file_name)[0] + '.png'
        png_path = os.path.join(output_folder, png_name)

        png_data = cairosvg.svg2png(url=svg_path, scale=8.0)

        with Image.open(io.BytesIO(png_data)) as img:

            add_transparent_background(img)
            img.save(png_path, format='PNG')
        print(f"Converted: {svg_path} -> {png_path}")

if __name__ == "__main__":
    input_folder = "themes/files"
    output_folder = "presence-icons"
    process_svgs(input_folder, output_folder)
