from docling.document_converter import DocumentConverter

def extract_text(document):
    converter = DocumentConverter()
    return converter.convert(document).document
    
def extract_text_from_pdf
