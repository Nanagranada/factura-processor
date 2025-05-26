# Procesador de Facturas para Helisa

Una aplicación web para automatizar el procesamiento de facturas y su integración con el software contable Helisa.

## Características

- Extracción automática de datos de facturas mediante OCR
- Procesamiento de facturas en formato PDF
- Generación de archivos compatibles con Helisa
- Sistema multiusuario con roles de administrador y usuario
- Interfaz web intuitiva y responsive

## Requisitos

- Python 3.8 o superior
- Flask y dependencias (ver requirements.txt)
- Tesseract OCR
- Poppler (para pdf2image)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Nanagranada/factura-processor.git
cd factura-processor
