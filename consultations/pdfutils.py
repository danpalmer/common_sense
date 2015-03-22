import io

from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter


def pdf_to_text(pdf_file):
    password = ''
    pagenos = set()
    maxpages = 0
    caching = True
    laparams = LAParams()

    rsrcmgr = PDFResourceManager(caching=caching)

    output = io.StringIO()
    out_device = TextConverter(rsrcmgr, output, laparams=laparams)

    process_pdf(
        rsrcmgr,
        out_device,
        pdf_file,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=True,
    )

    return out_device.getvalue()
