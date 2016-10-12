from pdfminer.pdfparser import PDFParser, PDFDocument, PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator, TextConverter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from io import StringIO
import PyPDF2

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
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # print(page_i, int(lt_obj.bbox[3] + 1), int(lt_obj.bbox[1]))
            # print(lt_obj.__class__.__name__)
            # print(lt_obj.get_text())

            text_snippet = TextSnippet(lt_obj.__class__.__name__,
                                       page_i,
                                       int(lt_obj.bbox[3]) + 1,
                                       int(lt_obj.bbox[1]),
                                       lt_obj.get_text())
            text_snippets.append(text_snippet) # TODO: don't append to list outside of fn
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj, page_i, text_snippets)  # Recursive

def open_document(filename):
    """For pdfminer, not for PyPDF2"""
    fp = open(filename, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')

    return doc

def make_snippets(document, page_num):
    """Input file path and get back TextSnippets for that single page"""
    # TODO: make work for multiple pages
    text_snippets = []

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page_i, page in enumerate(document.get_pages(), 1):
        if page_num <= page_i < page_num + 5:
            interpreter.process_page(page)
            layout = device.get_result()
            parse_layout(layout, page_i, text_snippets)

    return sorted(text_snippets)

def find_question_page_num(document, chapter, question):
    chapter_page = find_page_num(document, 'Chapter{}:'.format(chapter))
    return find_page_num(document, '{}.'.format(question), starting_page=chapter_page)

def find_page_num(filename, text, starting_page=0):
    ans = None

    pdf_file = open(filename, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()

    for page_i in range(1, number_of_pages + 1):
        if page_i >= starting_page:
            page = read_pdf.getPage(page_i - 1)
            page_content = page.extractText()
            if text.lower() in page_content.lower():
                ans = page_i
                break

    return ans
