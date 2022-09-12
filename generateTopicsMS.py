import pandas as pd
from utilities import util, LDATopicGen


# Topics microservice
# Given a piece of text, this microserivce will generate underlying latent topics.
# The model is stored and can be loaded & used for inference.

def generateTopics(dataSource):
    with open(dataSource) as f:
        text = f.readlines()

    data = pd.DataFrame(text, columns=['text'])
    column = 'text'

    #clean Data
    data = util.cleanData(data, column)

    #now get topics
    LDATopicGen.getTopics(data['tokens'])

if __name__ == "__main__":
    file = "./doc.txt"
    generateTopics(file)
