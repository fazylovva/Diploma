from random import randint

from django.core.cache import cache
from django.core.mail import EmailMessage


def _generate_activation_code():
    return randint(1000, 9999)


def send_code_email(subject, body, from_email, to):
    EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to
    ).send()


def send_code(email, cache_key: str, code: int):
    cache.set(f'{cache_key}_{email}', code, timeout=300)  # 5 min

    recipient = email
    send_code_email(
        subject='Activation code',
        body=f'Your code for activate email:: {str(code)}',
        from_email='womenssdiary@gmail.com',
        to=[recipient]
    )


def send_activation_code(request, email):
    code = _generate_activation_code()
    send_code(email, 'activate_email', code)
    return code
