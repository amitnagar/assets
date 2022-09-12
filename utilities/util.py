import re
import warnings
warnings.filterwarnings('ignore')
import re
from utilities import preprocessing as pre
import nltk
from nltk.corpus import stopwords
from utilities import preprocessing

# count NaN values under a single DataFrame column:
def countNaN_column(df, col):
    return df[col].isna().sum()

# count NaN values across a single DataFrame row:
def countNaN_row(df, row):
    return df.loc[[row]].isna().sum().sum()

# count NaN values under an entire DataFrame:
def  countNaN_df(df):
    return df.isna().sum().sum()

# remove given pattern
def remove_pattern(pattern, txt):
    return re.sub(pattern,'',txt)

# group by
def groupByCount(df, col1, col2):
    df = df.groupby(col1)[col2].count()
    c_dict = df.to_dict()
    if c_dict.get('UNITED STATES MINOR OUTLYING ISLANDS'):
        c_dict['US ISLANDS'] = c_dict.pop('UNITED STATES MINOR OUTLYING ISLANDS')
    return c_dict, df.shape[0]

# process text
def processTextForTopics(df, column):
  df['clean_msg'] = df[column].apply(lambda x: preprocessing.remove_punctuation(x))

  df['msg_lower'] = df['clean_msg'].apply(lambda x: x.lower())

  df['no_xxxx'] = df['msg_lower'].apply(lambda x: re.sub('xxxx','',x))

  #df['msg_tokenized'] = df['msg_lower'].apply(lambda x: preprocessing.tokenization(x))
  df['msg_tokenized'] = df['no_xxxx'].apply(lambda x: re.split('\W',x))

  stopwords = nltk.corpus.stopwords.words('english')
  df['tokens'] = df['msg_tokenized'].apply(lambda x: [i for i in x if i not in stopwords])
  

  df = df.drop(['clean_msg','msg_lower','msg_tokenized', 'no_xxxx'], axis=1)
  #df.columns=['product', 'consumer complaint narrative', 'tokens']
  
  return df

def cleanData(data, column):
  data = processTextForTopics(data, column)
  return data
