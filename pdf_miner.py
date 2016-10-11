from pdfminer.pdfparser import PDFParser, PDFDocument, PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure

class TextSnippet(object):
    def __init__(self, name, page, start_y, end_y, text):
        self.name = name
        self.page = page
        self.start = start_y
        self.end = end_y
        self.text = text

    def __lt__(self, other):
        return -1000*self.page + self.start > -1000*other.page + other.start # might have to reverse, do sth else to this equality

    def __repr__(self):
        return 'TextSnippet({}, {})'.format(self.page, self.start)

def parse_layout(layout, page_i, text_snippets):
    """Function to recursively parse the layout tree."""
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine) or True:
            print(page_i, int(lt_obj.bbox[3] + 1), int(lt_obj.bbox[1]))
            print(lt_obj.__class__.__name__)
            # print(lt_obj.get_text())

            # text_snippet = TextSnippet(lt_obj.__class__.__name__, page_i, int(lt_obj.bbox[3]) + 1, int(lt_obj.bbox[1]), lt_obj.get_text())
            # text_snippets.append(text_snippet) # TODO: don't append to list outside of fn
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj, page_num, text_snippets)  # Recursive

def make_snippets(filename, page_num):
    """Input file path and get back TextSnippets for that single page"""
    # TODO: make work for multiple pages
    text_snippets = []

    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page_i, page in enumerate(doc.get_pages()):
        interpreter.process_page(page)
        layout = device.get_result()
        parse_layout(layout, page_i, text_snippets)

    return sorted(text_snippets)
    # return text_snippets

def find_page_num(filename, chapter, question):
    """Get page num from question"""
    # TODO: complete this fn
    return page_num