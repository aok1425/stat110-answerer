from wand.image import Image
from wand.display import display
from pdfrw import PdfReader, PdfWriter
from base64 import b64encode

def take_snapshot(input_file, page_num, output_file, start_y, end_y, quality=5):
    with Image(filename=input_file, resolution=(72 * quality, 72 * quality)) as img_seq:
        img = Image(img_seq.sequence[page_num])
        img.resize(612, 792)
        img.crop(top=img.height - end_y, bottom=img.height - start_y, left=105, right=img.width - 105)
        img.format = 'png'
        img.save(filename=output_file)

def take_snapshots(snippets, input_file, temp_filename='tempfile.pdf'):
    correction_factor = sorted([i.page for i in snippets])[0]
    path = make_path(input_file)

    make_shortened_pdf(snippets, input_file, temp_filename)

    counter = 1

    for i,_ in enumerate(snippets[:-1]):
        if snippets[i+1].page == snippets[i].page:
            print('on snippet {}, temp{}'.format(i, counter))
            take_snapshot(path + temp_filename, snippets[i].page - correction_factor, path + 'temp{}.png'.format(counter), snippets[i+1].start, snippets[i].start)
            counter += 1

def make_shortened_pdf(snippets, input_file, temp_filename):
    infile = PdfReader(input_file)
    path = make_path(input_file)

    y = PdfWriter()
    for i, p in enumerate(infile.pages, 1):
        if i in [i.page for i in snippets]:
            y.addpage(p)
    y.write(path + temp_filename)

def take_snapshot(input_file, page_num, output_file, start_y, end_y, quality=5):
    with Image(filename=input_file, resolution=(72 * quality, 72 * quality)) as img_seq:
        img = Image(img_seq.sequence[page_num])
        img.resize(612, 792)
        img.crop(top=img.height - end_y, bottom=img.height - start_y, left=105, right=img.width - 105)
        img.format = 'png'
        return b64encode(img.make_blob()).decode()

def take_snapshots(snippets, input_file, temp_filename='tempfile.pdf'):
    correction_factor = sorted([i.page for i in snippets])[0]
    path = make_path(input_file)
    blobs = []

    make_shortened_pdf(snippets, input_file, temp_filename)

    counter = 1

    for i,_ in enumerate(snippets[:-1]):
        if snippets[i+1].page == snippets[i].page:
            print('on snippet {}, temp{}'.format(i, counter))
            blobs.append(take_snapshot(path + temp_filename, snippets[i].page - correction_factor, path + 'temp{}.png'.format(counter), snippets[i+1].start, snippets[i].start))
            counter += 1

    return blobs

def make_path(path):
    if '/' not in path:
        return path
    else:
        return input_file[:len(input_file) - input_file[::-1].index('/')]

# take_snapshot('/home/aok1425/Downloads/test2.pdf',
#               0,
#               '/home/aok1425/Downloads/test_snap.png',
#               0,
#               200,
#               quality=1)