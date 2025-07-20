
from django.conf import settings
def cleanup_email(email:str) -> str:

    if not settings.DEBUG and email.endswith('@example.com'):
        return email.split('@')[0] + '@gmail.com'

    return email