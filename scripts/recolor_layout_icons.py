import argparse
import os

from PIL import Image

'''
This script uses Pillow to recolor the Qtile layout icons
and drops them into `~/.config/qtile/layout-icons`.

$ python scripts/recolor_layout_icons.py --color "#E71E5E"

Once you've recolored the icons, you can use them
in the `CurrentLayoutIcon` widget, like so:

    widget.CurrentLayoutIcon(custom_icon_paths=[
        os.path.expanduser('~/.config/qtile/layout-icons/')
    ])

'''

ICON_SOURCE = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../libqtile/resources/layout-icons/'
))

ICON_DEST = os.path.expanduser('~/.config/qtile/layout-icons')


def recolor_icon(source, destination, color):
    img = Image.open(source)
    pixels = img.load()

    width, height = img.size

    for x in range(width):
        for y in range(height):
            if pixels[x, y] == (255, 255, 255, 255):
                pixels[x, y] = color

    img.save(destination)


def main(color):
    if not os.path.exists(ICON_DEST):
        os.makedirs(ICON_DEST)

    color = color.strip('#')
    rgb = tuple(map(lambda x: int(x, 16), (color[:2], color[2:4], color[4:6])))

    for filename in os.listdir(ICON_SOURCE):
        if filename.endswith('.png'):
            source = os.path.join(ICON_SOURCE, filename)
            destination = os.path.join(ICON_DEST, filename)
            recolor_icon(source, destination, rgb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Qtile layout icons to a specific color')
    parser.add_argument('--color', '-c', type=str, required=True,
                        help='Color in RGB hex format, with or without a preceding #.')

    args = parser.parse_args()
    main(args.color)
