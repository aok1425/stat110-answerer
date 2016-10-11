# from pdfminer.pdfparser import PDFParser, PDFDocument, PDFPage
# from pdfminer.pdfinterp import PDFResourceManager, PDFTextExtractionNotAllowed
# from pdfminer.pdfinterp import PDFPageInterpreter
# from pdfminer.pdfdevice import PDFDevice
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# import unicodedata, codecs

from pdfminer.pdfparser import PDFParser, PDFDocument, PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from io import StringIO

def getPDFText(pdfFilenamePath):
    retstr = StringIO()
    parser = PDFParser(open(pdfFilenamePath,'rb'))

    try:
        document = PDFDocument(parser)
    except Exception as e:
        print(pdfFilenamePath,'is not a readable pdf')
        return None

    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, retstr, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in document.get_pages():
        interpreter.process_page(page)

    return retstr.getvalue()

FILENAME = '/home/aok1425/Downloads/test.pdf'

retstr = StringIO()
lines = ''

fp = open(FILENAME, 'rb')
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
    rstr = retstr.getvalue()
    if len(rstr.strip()) > 0:
        lines += "".join(rstr)

lines