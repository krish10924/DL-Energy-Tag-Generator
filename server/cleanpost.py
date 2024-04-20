import re
from bs4 import BeautifulSoup as bs

def removeTag(soup, tagname):
    for tag in soup.findAll(tagname):
        contents = tag.contents
        parent = tag.parent
        tag.extract()
        
def cleanhtml(raw_html):
    soup = bs(raw_html, 'html.parser')
    code_tags = soup.find_all('code')
    code_text = ' '.join([code.get_text() for code in code_tags])

    return code_text

def remove_escape(text):
    esc = text.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ').replace("\'", ' ')
    return re.sub('\s+', ' ', esc)



def clean_code(data):
  data=remove_escape(data)
  b=cleanhtml(data)
  return b

def clean_body(data):
    cleaned_data = remove_escape(data)
    soup = bs(cleaned_data, "html.parser")
    removeTag(soup, 'a')
    removeTag(soup, 'code')
    text_content = soup.get_text()
    cleaned_text = text_content.strip()

    return cleaned_text

