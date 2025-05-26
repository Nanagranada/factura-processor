import pandas as pd
import os
from datetime import datetime
from app.utils.ocr import extract_invoice_data

def generate_helisa_file(pdf_path, invoice):
    """Genera un archivo Excel con el formato requerido por Helisa."""
    # Extraer datos de la factura si no se han extraído previamente
    if not invoice.invoice_number:
        invoice_data = extract_invoice_data(pdf_path)
    else:
        invoice_data = {
            'invoice_number': invoice.invoice_number,
            'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d') if invoice.invoice_date else '',
            'supplier_name': invoice.supplier_name,
            'supplier_id': invoice.supplier_id,
            'total_amount': invoice.total_amount
        }

    # Crear DataFrame para Helisa
    helisa_data = []

    # Registro de compra (débito)
    helisa_data.append({
        'TIPO DOC': 'FEV',
        'NÚMERO DE DOC': invoice_data['invoice_number'],
        'FECHA': invoice_data['invoice_date'],
        'CUENTA': '613595',  # Cuenta de compras (ejemplo)
        'CONCEPTO': f"Compra factura {invoice_data['invoice_number']}",
        'CENTRO DE COSTO': '001',  # Centro de costo (ejemplo)
        'VALOR': invoice_data['total_amount'] * 0.84,  # Valor sin IVA (ejemplo)
        'NATURALEZA': 'D',
        'IDENTIDAD TERCERO': invoice_data['supplier_id'],
        'NOMBRE DEL TERCERO': invoice_data['supplier_name'],
        'CLASE MOVIMIENTO': 'F'
    })

    # Registro de IVA (débito)
    helisa_data.append({
        'TIPO DOC': 'FEV',
        'NÚMERO DE DOC': invoice_data['invoice_number'],
        'FECHA': invoice_data['invoice_date'],
        'CUENTA': '240805',  # Cuenta de IVA (ejemplo)
        'CONCEPTO': f"IVA factura {invoice_data['invoice_number']}",
        'CENTRO DE COSTO': '001',  # Centro de costo (ejemplo)
        'VALOR': invoice_data['total_amount'] * 0.16,  # IVA (ejemplo)
        'NATURALEZA': 'D',
        'IDENTIDAD TERCERO': invoice_data['supplier_id'],
        'NOMBRE DEL TERCERO': invoice_data['supplier_name'],
        'CLASE MOVIMIENTO': 'F'
    })

    # Registro de cuenta por pagar (crédito)
    helisa_data.append({
        'TIPO DOC': 'FEV',
        'NÚMERO DE DOC': invoice_data['invoice_number'],
        'FECHA': invoice_data['invoice_date'],
        'CUENTA': '220505',  # Cuenta por pagar (ejemplo)
        'CONCEPTO': f"Cuenta por pagar factura {invoice_data['invoice_number']}",
        'CENTRO DE COSTO': '001',  # Centro de costo (ejemplo)
        'VALOR': invoice_data['total_amount'],
        'NATURALEZA': 'C',
        'IDENTIDAD TERCERO': invoice_data['supplier_id'],
        'NOMBRE DEL TERCERO': invoice_data['supplier_name'],
        'CLASE MOVIMIENTO': 'F'
    })

    # Crear DataFrame
    df = pd.DataFrame(helisa_data)

    # Crear directorio para archivos de salida si no existe
    output_dir = os.path.join(os.path.dirname(pdf_path), 'helisa_exports')
    os.makedirs(output_dir, exist_ok=True)

    # Generar nombre de archivo
    output_filename = f"helisa_import_{invoice_data['invoice_number']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xls"
    output_path = os.path.join(output_dir, output_filename)

    # Guardar como Excel
    df.to_excel(output_path, index=False)

    return output_path
