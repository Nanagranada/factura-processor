import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF utilizando OCR."""
    try:
        # Convertir PDF a imágenes
        images = convert_from_path(pdf_path)

        # Extraer texto de cada imagen
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang='spa')

        return text
    except Exception as e:
        print(f"Error al extraer texto del PDF: {e}")
        return ""

def extract_invoice_data(pdf_path):
    """Extrae datos relevantes de una factura."""
    text = extract_text_from_pdf(pdf_path)

    # Inicializar diccionario de datos
    invoice_data = {
        'invoice_number': '',
        'invoice_date': '',
        'supplier_name': '',
        'supplier_id': '',
        'total_amount': 0,
        'items': []
    }

    # Extraer número de factura
    invoice_number_patterns = [
        r'(?:Factura|FACTURA|Factura Electrónica|FACTURA ELECTRÓNICA).*?(?:No\.|N°|Nro\.|#)\s*:?\s*([A-Za-z0-9\-]+)',
        r'(?:No\.|N°|Nro\.|#)\s*:?\s*([A-Za-z0-9\-]+)'
    ]

    for pattern in invoice_number_patterns:
        match = re.search(pattern, text)
        if match:
            invoice_data['invoice_number'] = match.group(1).strip()
            break

    # Extraer fecha
    date_patterns = [
        r'(?:Fecha|FECHA|Date).*?:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            # Convertir a formato YYYY-MM-DD
            try:
                if '/' in date_str:
                    day, month, year = date_str.split('/')
                else:
                    day, month, year = date_str.split('-')

                if len(year) == 2:
                    year = '20' + year

                invoice_data['invoice_date'] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                # Si falla, intentar con formato YYYY-MM-DD
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    invoice_data['invoice_date'] = date_str
                except:
                    invoice_data['invoice_date'] = datetime.now().strftime('%Y-%m-%d')
            break

    # Extraer nombre del proveedor
    supplier_patterns = [
        r'(?:Proveedor|PROVEEDOR|Razón Social|RAZÓN SOCIAL).*?:\s*([A-Za-z0-9\s\.]+)',
        r'(?:Emisor|EMISOR).*?:\s*([A-Za-z0-9\s\.]+)'
    ]

    for pattern in supplier_patterns:
        match = re.search(pattern, text)
        if match:
            invoice_data['supplier_name'] = match.group(1).strip()
            break

    # Extraer NIT/ID del proveedor
    nit_patterns = [
        r'(?:NIT|Nit|nit).*?:\s*([0-9\.\-]+)',
        r'(?:ID|Identificación).*?:\s*([0-9\.\-]+)'
    ]

    for pattern in nit_patterns:
        match = re.search(pattern, text)
        if match:
            invoice_data['supplier_id'] = match.group(1).strip().replace('.', '').replace('-', '')
            break

    # Extraer monto total
    total_patterns = [
        r'(?:Total|TOTAL).*?:\s*\$?\s*([\d\.,]+)',
        r'(?:Valor Total|VALOR TOTAL).*?:\s*\$?\s*([\d\.,]+)'
    ]

    for pattern in total_patterns:
        match = re.search(pattern, text)
        if match:
            total_str = match.group(1).replace('.', '').replace(',', '.')
            try:
                invoice_data['total_amount'] = float(total_str)
            except:
                invoice_data['total_amount'] = 0
            break

    return invoice_data
