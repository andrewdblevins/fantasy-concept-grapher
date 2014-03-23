import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
from nltk.corpus import stopwords

X = pd.read_csv("spell_full.csv")
y = 

documents=spell_list['description']
stopWords = stopwords.words('english')
vectorizer = TfidfVectorizer(min_df=1,stop_words=stopWords)

selection = s

