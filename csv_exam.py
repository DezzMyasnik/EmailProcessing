import email

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

import settings
from recive_mail import email_text_extract
from recive_mail import exctaract_email, get_first_text_block


def clean_df(df):
    df = df.loc[~df['from'].isin(settings.droped_emails)]

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
    # result, data = post.fetch(item, "(RFC822)")  # Получаем тело письма (RFC822) для данного ID
    e_id = item.decode('utf-8')
    _, response = post.uid('fetch', e_id, '(RFC822)')
    raw_email = response[0][1]
    raw_email_string = raw_email.decode('utf-8', errors='replace')
    email_message = email.message_from_string(raw_email_string)
    to = item.decode('utf-8')
    from_ = exctaract_email(email_message['From'])
    if from_ in settings.droped_emails:
        predicted = ['nonreplay emails']
        return predicted, from_
    payload = get_first_text_block(email_message)
    if from_ == 'org.komitet@solncesvet.ru':
        payload, from_ = email_text_extract(payload)
    if payload != np.nan:
        try:

            predicted = text_clf.predict([payload])
        except BaseException as be:

            predicted = None
    else:

        predicted = None

    return predicted, from_


def return_type(email_text, model):
    predicted = model.predict(email_text)
    return predicted[0]
