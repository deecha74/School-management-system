from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings


def generate_fee_receipt(student_fee):
    """
    Generate a PDF receipt for the given student fee.
    """

    # Render the HTML template with the student fee data
    html_string = render_to_string('fee/fee_receipt.html', {'student_fee': student_fee})

    # Create a PDF from the rendered HTML
    pdf_file = HTML(string=html_string).write_pdf()

    # Save the PDF to a file or return it as a response
    receipt_filename = f"fee_receipt_{student_fee.student.id}.pdf"

    return pdf_file, receipt_filename