import numpy as np

from text_process import *

#получение email адреса из строки адреса. Там может быть и имя адресата, а оно лишнее
def exctaract_email(email_str):
    try:
        if '<' in email_str:
            to_ = email_str.split('<')
            to = to_[1][:-1]
        elif '@' in email_str:
            to = email_str
        else:
            to = None
        return to
    except BaseException as ex:
        print(ex)

def email_text_extract(post):
    """
    Парсинг сообщений с сайта из форм братной связи
    :param post: текст почтового сообщения из формы обратной связи
    :return:
    """
    email_text = ''
    try:
        found = re.search(r'Email:(.+?)Тема', post)
        found1 = re.search(r'Емайл:(.+?)Название', post)
        found2 = re.search(r'Email :(.+?)\r  Тема',post)
        found3 = re.search(r'Email :(.+?) Тема', post)
        if found:
            found = found.group(1)
            email_text = post[post.find('Сообщение: ') + 11:]
        elif found1:
            found = found1.group(1)
            email_text = post[post.find('Название работы: '):]
        elif found2:
            found = found2.group(1)
            email_text = post[post.find('Тема :'):]
        elif found3:
            found = found3.group(1)
            email_text = post[post.find('Тема :'):]


    except AttributeError:
        #found = re.search('Емайл:(.+?)Название работы:', post).group(1)

        #email_text = post[post.find('Название работы: ') + len('Название работы: '):]
        # AAA, ZZZ not found in the original string
        found = ''  # apply your error handling
        email_text = ''

    try:
        if email_text.isspace():
            email_text = ''
    except BaseException as ex:
        print(f'{ex}::: {post}')
    return (email_text, found.split()[0] if found else np.nan)

def remove_multiple_rr(text):
    return re.sub(r'\r+', ' ', text, flags=re.I)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# Необходимо преобразовать функцию к нормальному виду для работы в онлайне.
def proc_email_from_solncesvet():
    """
    Обработка сообщений из форм обратной связи
    :return:
    """
    parsing = get_post_from_email('org.komitet@solncesvet.ru', 'test_new.csv')
    # print(parsing.head(5))
    # dat = [remove_multiple_rr(text) for text in parsing['text'] if isinstance(text, str) ]
    for value in parsing.values:
        if isinstance(value[2], str):
            # id =  value.index
            text = remove_multiple_rr(value[2])
            text_email = email_text_extract(text)
            parsing.loc[parsing['Nom'] == value[0], 'text'] = text_email[0]
            parsing.loc[parsing['Nom'] == value[0], 'from'] = text_email[1]
            # parsing.loc[parsing['Nom'] == value[0]][1] = text_email[1]
            # parsing.loc[parsing['Nom'] == value[0]][0] = text_email[0]
        else:
            pass
    parsing.index = parsing['Nom']
    del parsing['Nom']
    parsing = parsing[parsing['from'] != '']
    parsing = parsing[parsing['from'].notna()]
    parsing = parsing[parsing['text'] != '']
    parsing = parsing[parsing['text'].notna()]
    # parsing.dropna(subset=['from'])
    parsing = parsing.drop_duplicates(subset=['from', 'text'])
    parsing.to_csv('solncesvet.csv')
    # parsing['cast'] = dat
    print(parsing.head(3))

#Получение текстового сообщения
def get_first_text_block(email_message_instance):
    returned_text = ''
    if not email_message_instance.is_multipart():
        returned_text = decode_body(email_message_instance.get_payload(),
                                    email_message_instance.get('Content-Transfer-Encoding'),
                                    email_message_instance.get_content_charset())
    else:
        pyaloads = email_message_instance.get_payload()
        for payload in pyaloads:
            maintype = payload.get_content_maintype()
            disposition = payload.get_content_disposition()
            if maintype == 'text' and disposition != 'attachment':
                returned_text = decode_body(payload.get_payload(),
                                            payload.get('Content-Transfer-Encoding'),
                                            payload.get_content_charset())
            elif maintype == 'multipart':
                returned_text = ' '.join([get_first_text_block(item) for item in payload.get_payload()])

                #text = ''
                #for item in payload.get_payload():
                #    text = text + get_first_text_block(item)


                #returned_text = text

    returned_text = remove_multiple_spaces(remove_multiple_rr(returned_text))
    return returned_text