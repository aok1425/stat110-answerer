from wand.image import Image
from wand.display import display
from pdfrw import PdfReader, PdfWriter

PADDING = 10

resolution = 300
resolution = 100

def take_snapshot(input_file, output_file, start_y, end_y):
    # start_y and end_y don't involve img.height
    with Image(filename=input_file) as img:
        # img.resize(int(img.width * 100 / resolution), int(img.height * 100 / resolution))
        # top = 120*3 at min
        # img.crop(left=175, right=img.width - 175, top=img.height - 710 - PADDING, bottom=img.height - 605)
        print(img.width, img.height)
        img.crop(top=img.height - end_y, bottom=img.height - start_y)
        # img.compression_quality = 2
        img.format = 'png'
        img.save(filename=output_file)
        # img.make_blob()

def take_snapshot(input_file, page_num, output_file, start_y, end_y):
    with Image(filename=input_file) as img_seq:
        img = Image(img_seq.sequence[page_num])
        img.crop(top=img.height - end_y, bottom=img.height - start_y)
        img.format = 'png'
        img.save(filename=output_file)

def take_snapshots(snippets, input_file, temp_filename='tempfile.pdf'):
    correction_factor = sorted([i.page for i in snippets])[0]
    path = input_file[:len(input_file) - input_file[::-1].index('/')]

    make_shortened_pdf(snippets, input_file, temp_filename)

    counter = 1

    for i,_ in enumerate(snippets[:-1]):
        if snippets[i+1].page == snippets[i].page:
            print('on snippet {}, temp{}'.format(i, counter))
            take_snapshot(path + temp_filename, snippets[i].page - correction_factor, path + 'temp{}.png'.format(counter), snippets[i+1].start, snippets[i].start)
            counter += 1

def make_shortened_pdf(snippets, input_file, temp_filename):
    infile = PdfReader(input_file)
    path = input_file[:len(input_file) - input_file[::-1].index('/')]

    y = PdfWriter()
    for i, p in enumerate(infile.pages, 1):
        if i in [i.page for i in snippets]:
            y.addpage(p)
    y.write(path + temp_filename)