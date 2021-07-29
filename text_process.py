
import base64
import locale
import csv
import os
import quopri
preferredencoding = locale.getpreferredencoding()
import pandas as pd
from html.parser import HTMLParser
from html.entities import name2codepoint
import re


class MyHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs ):
        self.dataa = ''
        super().__init__()

    def handle_data(self, data):
        if not data.startswith(('.class','<!--')):
            self.dataa = self.dataa + data
            return (data)
        else:
            return (data)

    def return_data(self):
        return self.dataa


def remove_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text, flags=re.I)


def remove_re_email(text):
    text = text.replace('\t', '')
    #text = remove_multiple_spaces(text)
    temp_list = text.split('\n')
    for item in reversed(temp_list):
        if item.startswith('>'):
            temp_list.remove(item)
    return ' '.join(temp_list)


def decode_body(text, content_transfer_encoding, content_charset):
    error = 0
    parser = MyHTMLParser()
    if content_charset is None:
        content_charset = preferredencoding
    try:
        if content_transfer_encoding == 'quoted-printable':
            text = quopri.decodestring(text)
            text = text.decode(content_charset)
        elif content_transfer_encoding == 'base64':
            text = base64.b64decode(text)
            try:
                text = text.decode('utf_8_sig')
            except Exception as err:
                text = ''
                error = err

    except Exception as err:
        text = str(text)
        error = err

    parser.feed(text)
    text = parser.dataa
    text = remove_re_email(text)
    return text


def write_header_to_csv(name):
    if not os.path.exists(name):
        with open(name, "a", newline="", encoding='utf_8_sig') as file:
            fieldnames = ['Nom', 'from', 'text', 'Class']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', )
            writer.writeheader()


def write_to_csv(name, csv_str):
    with open(name, "a", newline="", encoding='utf_8_sig') as file:
        fieldnames = ['Nom', 'from', 'text','Class']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';', )
        writer.writerow(csv_str)


def get_last_email_from_csv(name):
    #post_review.shape()
    if os.path.exists(name):
        post_review = pd.read_csv(name, sep=';')
        return max(0, post_review['Nom'].max())



def get_post_from_email(email,name):
    post_reviews = pd.read_csv(name, sep=';')
    return post_reviews.loc[(post_reviews['from'] == email)]

def del_from_csv(email,name):
    post_reviews = pd.read_csv(name, sep=';')
    return post_reviews.loc[(post_reviews['from'] != email)]
