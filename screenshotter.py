from wand.image import Image
from wand.display import display

PADDING = 10

resolution = 300
resolution = 100

def take_snapshot(filename, start_y, end_y):
    # start_y and end_y don't involve img.height
    with Image(filename=filename) as img:
        # img.resize(int(img.width * 100 / resolution), int(img.height * 100 / resolution))
        # top = 120*3 at min
        # img.crop(left=175, right=img.width - 175, top=img.height - 710 - PADDING, bottom=img.height - 605)
        img.crop(top=img.height - end_y, bottom=img.height - start_y)
        # img.compression_quality = 2
        img.format = 'png'
        img.save(filename='/home/aok1425/Downloads/temp.png')
        # img.make_blob()