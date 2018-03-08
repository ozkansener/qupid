"""
Ozkan Sener
ozkansener@gmail.com
OOk met vier clusters
"""
from flask_restplus import Namespace, Resource, fields
from multiprocessing.dummy import Pool as ThreadPool
import requests
import pandas as pd
from newspaper import Article
import re
from MagicGoogle import MagicGoogle
import json
import pandas as pd
from newspaper import Article
from bs4 import BeautifulSoup
import urllib.request
import newspaper
import re
import numpy as np
import itertools
import pandas as pd
from joblib import Parallel, delayed
from queue import Queue
from threading import Thread
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time
from sklearn.metrics.pairwise import cosine_similarity
import time



api = Namespace('Multiple', description='Multiple Documents Web documents')

multi = api.model('url', {
    'url': fields.String(required=True, description='The Query entifier'),
    'topic': fields.String(required=True, description='Topic'),
    'clusters': fields.String(required=True, description='Cluster'),
    'time': fields.String(required=True, description='Time'), })


# called by each thread
def get_web_data(url):
    n = 0
    seconds = 5
    while n < seconds + 1:
        n += 1
        try:
            start = time.time()
            article = Article(url)
            article.download()
            article.parse()
            end = time.time()
            tijd = (end - start)
            date=article.publish_date
            text = article.text
            re.sub("[^0-9a-zA-Z]", " ", text)
            filter(lambda x: not re.match(r'^\s*$', x), text)
            return {'url': url, 'tekst': text, 'time': round(tijd)}


        except:
            if n == seconds:
                return {'url': 'not', 'tekst': 'not'}


@api.route('/<Query>')
@api.param('Query', 'The multi Queryentifier')
@api.response(404, 'multi not found')
class multi(Resource):
    @api.doc('get_list_multi')
    @api.marshal_list_with(multi)
    def get(self, Query):
        mg = MagicGoogle()
        urls = []
        search = str(Query + ' language:english file:html')
        print(search)
        for url in mg.search_url(query=search):
            urls.append(str(url))
        tel=len(urls)
        pool = ThreadPool(tel)
        result = pool.map(get_web_data, urls)
        df1 = pd.DataFrame(result)
        df1 = df1[df1['tekst'].notnull()]
        print(len(df1.index))
        tekst=df1.tekst.values.tolist()
        df1.drop(['tekst'], axis=1, inplace=True)
        #cat = df1['label'].values
        aantal = len(tekst)
        #print(aantal)
        #print(aantal)

        n_samples = 5000
        n_features = 2000
        n_components = aantal
        n_top_words = 5

        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                        max_features=n_features,
                                        stop_words='english')
        tf= tf_vectorizer.fit_transform(tekst)
        tf_feature_names = tf_vectorizer.get_feature_names()
        lda = LatentDirichletAllocation(n_components=n_components, max_iter=30,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)

        lda.fit(tf)
        ozzy = []

        def print_top_words(model, feature_names, n_top_words):
            # ozzy = []
            for topic_idx, topic in enumerate(model.components_):
                oz = (" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
                ozzy.append(oz)
        print_top_words(lda, tf_feature_names, n_top_words)
        df1['topic'] = ozzy



        true_k = int(aantal * 0.3)
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
        km.fit(tf)
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = tf_vectorizer.get_feature_names()
        jk = []
        for i in range(true_k):
            j = []
            jk.append(j)
            for ind in order_centroids[i, :7]:
                za = str(' %s' % terms[ind])
                j.append(za)

        cols = {'clusters': jk}
        df2 = pd.DataFrame.from_dict(cols)
        df2['clusters'] = df2['clusters'].astype(str).str.replace(r"[\[\]']", '')  # terms
        df2.insert(0, 'clusterid', range(0, 0 + len(df2)))

        labels = km.labels_
        df1['clusterid'] = labels
        dfs = pd.merge(df1, df2)
        dfs.drop(['clusterid'], axis=1, inplace=True)
        multiS = dfs.to_dict()
        return multiS
        # from sklearn.naive_bayes import MultinomialNB
        # # clf = MultinomialNB().fit(tf, cat)
        # from sklearn.externals import joblib
        # # joblib.dump(clf, 'filename.pkl')
        # clf = joblib.load('filename.pkl')
        # # ttf = tf
        # cats = clf.predict(tf)
        # # # acc=np.mean(predicted == cat)
        # cm = metrics.confusion_matrix(cat, predicted)
        # sim = cosine_similarity(tf)

        '''Fetch a multi given its Queryentifier'''
        api.abort(404)

