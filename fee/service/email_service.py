

from fee.service.pdf_service import generate_fee_receipt


def sent_fee_receipt_email(student_fee, recipient_email):
    """
    Send an email with the fee receipt to the student.
    """
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    from django.conf import settings

    # Generate the PDF receipt
    pdf_file, receipt_filename = generate_fee_receipt(student_fee)

    # Create the email content
    subject = f"Fee Receipt for {student_fee.student.name}"
    message = render_to_string('fee/fee_receipt_email.html', {'student_fee': student_fee})

    # Create the email
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
    )

    # Attach the PDF file
    email.attach(receipt_filename, pdf_file, 'application/pdf')

    # Send the email
    email.send()