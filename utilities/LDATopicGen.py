import gensim
from gensim import corpora
from gensim import models
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# method to extract topics given data

def getTopics(data):

  dictionary = gensim.corpora.Dictionary(data)
  bow_corpus = [dictionary.doc2bow(doc) for doc in data] 
  tfidf = models.TfidfModel(bow_corpus)
  corpus_tfidf = tfidf[bow_corpus]

  lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

  # print topics
  for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))

  # save the model to disk
  filename = 'model.sav'
  pickle.dump(lda_model, open(filename, 'wb'))

  return