import re
 
import pandas as pd
#from sklearn.datasets import fetch_20newsgroups
import string
string.punctuation
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')



#punctuation
def remove_punctuation(text):
    noPunctuation="".join([i for i in text if i not in string.punctuation])
    return noPunctuation

#tokenization
def tokenization(text):
    tokens=re.split('\W',text)
    return tokens

#Stop words
def remove_stopwords(text):
    output=[i for i in text if i not in stopwords]
    return output

#stemming - not always a good idea as it loses the word meaning after stemming
def stemming(text):
    stemText=[porterStemmer.stem(word) for word in text]
    return stemText

#Lemmatization - stems but does not lose its meaning
def lemmatizer(text):
    lemmText=[wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemmText


def cleanText(text):

    # if data is None:
    #     data=pd.DataFrame(text)
    #     data.columns=['message']

    data=pd.DataFrame([text])
    data.columns=['message']

    print(data)
    print('\n')

    data['clean_msg'] = data['message'].apply(lambda x: remove_punctuation(x))

    data['msg_lower'] = data['clean_msg'].apply(lambda x: x.lower())

    data['msg_tokenized'] = data['msg_lower'].apply(lambda x: tokenization(x))

    stopwords = nltk.corpus.stopwords.words('english')
    data['no_stopwords'] = data['msg_tokenized'].apply(lambda x: remove_stopwords(x))


    # porterStemmer = PorterStemmer()
    # data['msg_stemmed'] = data['no_stopwords'].apply(lambda x: stemming(x))
    #
    wordnet_lemmatizer = WordNetLemmatizer()
    data['msg_lemmatized']=data['no_stopwords'].apply(lambda x:lemmatizer(x))
    print(data)

if __name__ == "__main__":
    text = "over the course of 30 days i have filed a dispute in regards to inaccurate and false information on my credit report ive attached a copy of my dispute mailed in certified to equifax and they are still reporting these incorrect items according to the fair credit act section 609 a 1 a they are required by federal law to only report accurate information and the have not done so they have not provided me with any proof ie and original consumer contract with my signature on it proving that this is my account\n\nfurther more i would like to make a formal complaint that ive tried calling equifax over 10 times this week and every single time ive called ive asked for a representative in the fraud dispute department wants transfer it over there when you speak to the representative and let them know that you are looking to dispute inquiries and accounts due to fraud they immediately transfer you to their survey line essentially ending the call i believe equifax is training their representatives to not help consumers over the phone and performing unethical practices \n\nonce i finally got a hold of a representative she told me that she could not help because i did not send in my social security card which violates my consumer rights so im making a formal cfpb complaint that you will correct equifaxs actions \n\nbelow ive written what is also included in the files uploaded my disputes for inaccuracies on my credit report"
    print(tokenization(text))
    #print(re.split('\W', 'hello world'))