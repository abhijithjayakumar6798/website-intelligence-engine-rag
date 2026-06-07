import re


def clean_content(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()