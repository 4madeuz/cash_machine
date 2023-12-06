import jinja2
import qrcode
import pdfkit
from django.conf import settings
from django.db.models import QuerySet, Model
from typing import AnyStr


def form_pdf_file(items: QuerySet, receipt: Model):
    template_loader = jinja2.FileSystemLoader(searchpath="app/templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('receipt2.html')
    html_content = template.render({'items': items, 'total_price': receipt.total_price, 'timestamp':receipt.created_at.strftime('%d.%m.%y %H:%M')})
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    pdf_file_path = f'media/receipt{receipt.id}.pdf'
    pdfkit.from_string(html_content, pdf_file_path, configuration=config)
    return pdf_file_path


def form_qr_code(pdf_file_path: AnyStr,  receipt: Model):
    base_url = settings.BASE_URL
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
    qr.add_data(f'{base_url}/{pdf_file_path}')
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")
    qr_code_path = f'media/qrcode_{receipt.id}.png'
    qr_code.save(qr_code_path)
    return qr_code_path