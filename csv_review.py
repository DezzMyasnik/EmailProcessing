import pandas as pd
import os
import matplotlib.pyplot as plt
import string
import re
from collections import Counter
import nltk
from nltk.stem import *
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from tqdm.auto import tqdm, trange
import pymorphy2
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import HashingVectorizer
from nltk import word_tokenize



def tokenizer(x):
    return ( w for w in word_tokenize(x) if len(w) >3)


#nltk.download()
# def lemmatize_text(text):
#    tokens = mystem.lemmatize(text.lower())
#    tokens = [token for token in tokens if token not in russian_stopwords and token != " "]
#    text = " ".join(tokens)
#    return text
def generate_wordcoud(df,stopwords):
    texts = ' '.join(df['tokenize'])
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(texts)
    # построить изображение WordCloud
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def read_csv_test(name):
    if os.path.exists(name):
        post_review = pd.read_csv(name, sep=';')
        return post_review

    else:
        return None


def write_csv(pd, name):
    pd.to_csv(name, sep=';')


def remove_punctuation(text):
    return "".join([ch if ch not in string.punctuation else ' ' for ch in text])


def remove_numbers(text):
    return ''.join([i if not i.isdigit() else ' ' for i in text])


def remove_multiple_spaces(text):
    return re.sub(r'\s+', ' ', text, flags=re.I)


def remove_re_email(text):
    temp_list = text.split('\n')

    eng_alph = 'abcdefghijklmnopqrstuvwxyz<.'
    eng_alph = tuple(list(eng_alph))
    for item in reversed(temp_list):
        if item.startswith('>') :
            temp_list.remove(item)

    return ' '.join(temp_list)

def f_tokenizer(s):
    morph = pymorphy2.MorphAnalyzer()
    ee = type(s)
    if type(s) == str:
        t = s.split(' ')
    else:
        t = s
    f = []
    for j in t:
        m = morph.parse(j.replace('.', ''))
        if len(m) != 0:
            wrd = m[0]
            if wrd.tag.POS not in ('NUMR', 'PREP', 'CONJ', 'PRCL', 'INTJ'):
                f.append(wrd.normal_form)
    f = ' '.join(f)
    return f

def clean_df(df):
    droped_emails = ['no_reply@free-lance.ru',
                     'info@r.molodost.bz',
                     'info@jivosite.com',
                     'info@emailstream.ru',
                     'donotreplyconsumer.relations@gsk.com',
                     'mailer-daemon@corp.mail.ru',
                     'info@pedsovet.su',
                     'notification@russianpost.ru',
                     'alert@uptimerobot.com',
                     'mzs@r.molodost.bz',
                     'support@miran.ru',
                     'no_reply@free-lance.ru',
                     'support@sendpulse.com',
                     'mailer-daemon@googlemail.com',
                     'noreply.otpravka@russianpost.ru',
                     'info@vitvet.com',
                     'open@garant.ru',
                     'info@seoslon.com',
                     'serafim@rzdtour.com',
                     'mihail.dashkiev@r.molodost.bz',
                     'petr.osipov@r.molodost.bz',
                     'noreply@hypercomments.com']

    df = df.loc[~df['from'].isin(droped_emails)]

    return df





#russian_stopwords = stopwords.words("russian")
#english_stopwords = stopwords.words('english')
#df = read_csv_test('test_new3.csv')
#df = df.iloc[:500]
#df = clean_df(df)
#df = df.dropna(axis='index', how='any', subset=['text'])
#cleaned = [remove_re_email(text) for text in tqdm(df['text'])]
#df['cleaned'] = cleaned
#del df['text']
#write_csv(df, 'out3.csv')
#prep_text = [remove_multiple_spaces(remove_numbers(remove_punctuation(text.lower()))) for text in tqdm(df['cleaned'])]
#df['text_prep'] = prep_text
#tok = [f_tokenizer(text) for text in tqdm(df['text_prep'])]
#df['tokenize'] = tok


#from nltk.stem.snowball import SnowballStemmer
#stemmer = SnowballStemmer("russian")
#russian_stopwords.extend(['здравствуйте', 'спасибо',"добрый", "день"])
#stemmed_texts_list = []
#for text in tqdm(df['text_prep']):
#    tokens = word_tokenize(text)
#    stemmed_tokens = [stemmer.stem(token) for token in tokens if token not in russian_stopwords]
#    text = " ".join(stemmed_tokens)
#    stemmed_texts_list.append(stemmed_tokens)

#df['text_stem'] = stemmed_texts_list
""""
mystem = Mystem()
lemm_texts_list = []
for text in tqdm(df['text_stem']):
    # print(text)
    try:
        text_lem = mystem.lemmatize(text)
        tokens = [token for token in text_lem if token != ' ' and token !='\n' and token not in russian_stopwords]
        text = " ".join(tokens)
        lemm_texts_list.append(tokens)
    except Exception as e:
        print(e)

df['text_lemm'] = lemm_texts_list


#from gensim.models import Word2Vec


w2v_model = Word2Vec(
    min_count=2,
    window=2,
    vector_size=30,
    negative=10,
    alpha=0.03,
    min_alpha=0.0007,
    sample=6e-5,
    sg=1)
w2v_model.build_vocab(df['text_stem'])
w2v_model.train(df['text_stem'], total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
''''

def get_vector_of_post(model,text):
    vectors_ =[]

    for word in text:
        try:
            vectors = model.wv.get_vector(word)
            vectors_.append(vectors)

        except KeyError:
            pass
        #words = [word]
    ss = sum(vectors_)
    return ss

def tsne_plots(model,list_posts):
    list_post_2_list = list_posts.tolist()
    out_vectors = [get_vector_of_post(model,text) for text in tqdm(list_posts) if len(text) != 0]
    color_list = ['red']*len(out_vectors)
    Y = (TSNE(n_components=2, random_state=0, perplexity=15, init="pca")
         .fit_transform(out_vectors))

    xx = [x for x in Y[:, 0]]
    yy = [y for y in Y[:, 1]]
    df_ = pd.DataFrame({"x": xx,
                        "y": yy,
                        "color": color_list})

    fig, _ = plt.subplots()
    fig.set_size_inches(9, 9)
    # Basic plot
    p1 = sns.regplot(data=df_,
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="o",
                     scatter_kws={"s": 40,
                                  "facecolors": df_["color"]})

    # Adds annotations one by one with a loop
    #unk = df_.shape[0]

    for line in range(0, df_.shape[0]):
        s = f"{' '.join(list_post_2_list[line])}"
        p1.text(df_["x"][line],
                df_["y"][line],
                s,
                horizontalalignment="left",
                verticalalignment="bottom", size="medium",
                color=df_["color"][line],
                weight="normal"
                ).set_size(15)
    plt.xlim(Y[:, 0].min() - 50, Y[:, 0].max() + 50)
    plt.ylim(Y[:, 1].min() - 50, Y[:, 1].max() + 50)
    plt.title('t-SNE visualization for ')
    plt.show()

def tsne_scatterplot(model, word, list_names):
    Plot in seaborn the results from the t-SNE dimensionality reduction
    algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    vectors_words = [model.wv[word]]
    word_labels = [word]
    color_list = ['red']
    close_words = model.wv.most_similar(word)
    for wrd_score in close_words:
        wrd_vector = model.wv[wrd_score[0]]
        vectors_words.append(wrd_vector)
        word_labels.append(wrd_score[0])
        color_list.append('blue')
    # adds the vector for each of the words from list_names to the array
    for wrd in list_names:
        wrd_vector = model.wv[wrd]
        vectors_words.append(wrd_vector)
        word_labels.append(wrd)
        color_list.append('green')
    # t-SNE reduction
    Y = (TSNE(n_components=2, random_state=0, perplexity=15, init="pca")
        .fit_transform(vectors_words))
    # Sets everything up to plot
    df = pd.DataFrame({"x": [x for x in Y[:, 0]],
                    "y": [y for y in Y[:, 1]],
                    "words": word_labels,
                    "color": color_list})
    fig, _ = plt.subplots()
    fig.set_size_inches(9, 9)
    # Basic plot
    p1 = sns.regplot(data=df,
                    x="x",
                    y="y",
                    fit_reg=False,
                    marker="o",
                    scatter_kws={"s": 40,
                                "facecolors": df["color"]}
    )
    # Adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
        p1.text(df["x"][line],
                df["y"][line],
                " " + df["words"][line].title(),
                horizontalalignment="left",
                verticalalignment="bottom", size="medium",
                color=df["color"][line],
                weight="normal"
        ).set_size(15)
    plt.xlim(Y[:, 0].min()-50, Y[:, 0].max()+50)
    plt.ylim(Y[:, 1].min()-50, Y[:, 1].max()+50)
    plt.title('t-SNE visualization for {}'.format(word.title()))
    plt.show()

#tsne_plots(w2v_model,df['text_stem'])
#get_vector_of_post(w2v_model,df['text_stem'][23])
#tsne_scatterplot(w2v_model, "диплом", ['личный', 'кабинет'])
#coder = HashingVectorizer(tokenizer=f_tokenizer, n_features=256)

#trn = coder.fit_transform(df['tokenize'].tolist()).toarray()
"""
#wc = count(prep_text)

#import seaborn as sns
#sns.lineplot(x = 'rank', y = 'cul_pct_total', data = wc)
#plt.show()
#print(wc.head(20))


#import squarify
#wc_top20 = wc[wc['rank'] <= 20]
#squarify.plot(sizes=wc_top20['pct_total'], label=wc_top20['word'], alpha=.8 )
#plt.axis('off')
#plt.show();

#russian_stopwords.extend(['солнечный','свет','komitet','solncesvet'])
#generate_wordcoud(df,russian_stopwords+english_stopwords)
#выявление статистики слов в письмах
#commonwords = pd.Series(' '.join(df['tokenize']).lower().split()).value_counts()[:100]

#write_csv(commonwords,'stat2.csv')
#print(trn)

#print(df.head(6))



# pr.text = pr.text.str.lower()

# print(pr.head(5))
# dd = pr['from'].value_counts()
# df = dd.iloc[:100]
# df.plot(kind='bar', x='', y='from')
# plt.show()
