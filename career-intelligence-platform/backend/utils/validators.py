import re


def validate_email(email):
    """
    Validate email format
    """

    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    return bool(
        re.match(pattern, email)
    )


def validate_password(password):
    """
    Password requirements:
    - Minimum 8 chars
    - One uppercase
    - One lowercase
    - One digit
    """

    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    return True


def validate_resume_text(text):

    if not text:
        return False

    if len(text.strip()) < 100:
        return False

    return True