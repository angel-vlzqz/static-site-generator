import re

# takes in markdown text and returns a list of tuples containing the alt text,
# and link
def extract_markdown_images(text):
    alt_text = re.findall(r"\[(.*?)\]", text)
    link_text = re.findall(r"\((.*?)\)", text)
    matches = zip(alt_text, link_text)

    return list(matches)

def extract_markdown_links(text):
    alt_text = re.findall(r"\[(.*?)\]", text)
    link_text = re.findall(r"\((.*?)\)", text)
    matches = zip(alt_text, link_text)

    return list(matches)

