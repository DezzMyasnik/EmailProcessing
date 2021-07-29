import email
import email.utils
import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from settings import *
from recive_mail import email_text_extract
from recive_mail import exctaract_email, get_first_text_block


def clean_df(df):
    df = df.loc[~df['from'].isin(droped_emails)]

    return df


def make_model(csv_df):
    my_tags = []
    for i, item in enumerate(csv_df['Class'].unique()):
        my_tags.append([i, item])
    data_fr = pd.DataFrame(data=my_tags, columns=['Num', 'Class'])
    train_csv = csv_df.merge(data_fr, how='outer', left_on='Class', right_on='Class')
    y = list(train_csv['Class'].unique())
    from sklearn.linear_model import SGDClassifier
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge',
                                               penalty='l2',
                                               alpha=1e-3,
                                               max_iter=300,
                                               random_state=42)),
                         ])

    text_clf = text_clf.fit(train_csv.text, train_csv.Class)
    return text_clf


def my_custom_loss_func(y_true, y_pred):
    diff = np.abs(y_true - y_pred).max()
    return np.log1p(diff)


def get_class_of_email(item, post, text_clf):
    _, response = post.uid('fetch', item.decode('utf-8'), '(RFC822)')
    raw_email_string = response[0][1].decode('utf-8', errors='replace')
    email_message = email.message_from_string(raw_email_string)
    dt_email_tz =email.utils.parsedate_to_datetime(email_message['Date'])
    from_ = exctaract_email(email_message['From'])
    payload = get_first_text_block(email_message)

    if from_ in droped_emails:
        predicted = ['nonreplay emails']
        return predicted, from_, dt_email_tz, payload
    if payload == '' or payload == None or payload == ' ':
        predicted = ['Только вложения']
        return predicted, from_, dt_email_tz, payload
    if from_ == EMAIL_FROM_FORM:
        payload, from_ = email_text_extract(payload)
    if from_ == ' offline-messages@jivosite.com':
        predicted = ['Из чата сайта']
        return predicted, from_, dt_email_tz, payload
    if payload != np.nan:
        try:
            predicted = text_clf.predict([payload])
        except BaseException as be:

            predicted = None
    else:

        predicted = None

    return predicted, from_, dt_email_tz,payload


def return_type(email_text, model):
    predicted = model.predict(email_text)
    return predicted[0]
