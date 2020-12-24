# MIT License

# Copyright (c) 2020 Shrid Pant

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PIL import Image, ImageDraw, ImageFont
import textwrap, os

def meme(para = 'Hello, World!'):
    # INPUT
    im = Image.open('static/meme/cat.jpg')

    # CONFIGURATION
    image_width, image_height = im.size
    arial = ImageFont.truetype("arial.ttf", size = 120)
    draw = ImageDraw.Draw(im)
    shadowcolor = 'black'
    fillcolor = 'white'
    highlight_width = 5

    # MULTILINE
    paragraph = textwrap.wrap(str(para), initial_indent = '(output) ', placeholder = 'etc etc ...', width = 25, max_lines = 3, break_long_words = True)
    initial_height, line_spacing = (0.01 * image_height), 1
    for line in paragraph:
        text_width, text_height = draw.textsize(line, font = arial)
        x_coordinate, y_coordinate = (image_width - text_width) / 2, initial_height
        draw.text((x_coordinate - highlight_width, y_coordinate - highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate + highlight_width, y_coordinate - highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate - highlight_width, y_coordinate + highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate + highlight_width, y_coordinate + highlight_width), line, font = arial, fill=shadowcolor)
        draw.text((x_coordinate, y_coordinate), line, font = arial, fill = fillcolor)
        initial_height += text_height + line_spacing

    # OUTPUT
    im.save('static/meme/output.png', "PNG")