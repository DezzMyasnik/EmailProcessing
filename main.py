import csv
import email
import imaplib
from settings import *
from text_process import *
from recive_mail import *
import re
import pandas as pd
import numpy as np
from csv_exam import *



def main_proc(last_email, name):
    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(user, password)
    mail.list()
    mail.select('inbox')
    result, data = mail.search(None, "ALL")
    ids = data[0]  # Получаем строку номеров писем
    id_list = ids.split()  # Разделяем ID писем
    #latest_email_id = id_list[-1]  # Берем последний ID

    write_header_to_csv(name)
    train_csv = pd.read_csv('Classyfy_.csv', sep=';')

    text_clf = make_model(train_csv)

    for item in reversed(id_list):
        if int(item) > 125001:
            from_, payload, predicted, to = get_class_of_email(item, mail, text_clf)
            csv_str = {'Nom': to, 'from': from_, 'text': payload, 'Class': predicted[0]}
            write_to_csv(name, csv_str)





def main_one_email(number):
    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(user, password)
    mail.list()
    mail.select('inbox')
    result, data = mail.fetch(str(number), "(RFC822)")  # Получаем тело письма (RFC822) для данного ID
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8', errors='replace')
    #with open('temp.eml','w') as file:
    #    file.write(raw_email_string)
    email_message = email.message_from_string(raw_email_string)
    to = number
    from_ = exctaract_email(email_message['From'])
    payload = get_first_text_block(email_message)
    return (payload, from_)
    #print(f'{to}\t{from_}\t{payload}')










if __name__ == '__main__':
    #proc_email_from_solncesvet()
    #df1 = pd.read_csv('solncesvet.csv')
    #df2 = del_from_csv('org.komitet@solncesvet.ru', 'test_new.csv')
    #df3 =  pd.concat([df1,df2])
    #df3.index = df3['Nom']
    #del df3['Nom']
    #df3.to_csv('test_new3.csv',sep=";")
    #print(df3.head(10))

    #main_one_email(131350)
    last_email_index = get_last_email_from_csv('test_new.csv')
    main_proc(last_email_index,'test_new.csv')


