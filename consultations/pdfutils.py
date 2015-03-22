import io

from pdfminer.layout import LAParams
from pdfminer.psparser import PSEOF
from pdfminer.pdfparser import PDFEncryptionError
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter


def pdf_to_text(pdf_file):
    password = ''
    pagenos = set()
    maxpages = 0
    caching = True
    laparams = LAParams()

    rsrcmgr = PDFResourceManager(caching=caching)

    with io.StringIO() as output:
        out_device = TextConverter(rsrcmgr, output, laparams=laparams)

        try:
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
        except PSEOF:
            raise ValueError("Invalid PDF")
        except PDFEncryptionError:
            raise ValueError("Bad encryption")

        return output.getvalue()
