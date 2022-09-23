from scipy.stats.distributions import cosine
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

def sentenceEmbedding(sentence):
  model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

  #Sentences are encoded by calling model.encode()
  embedding = model.encode(sentence)

  return embedding

def compare_word_embeddings(embedding1, embedding2):
  similarity = 1 - cosine(embedding1, embedding2)
  print('Similarity between the 2 embeddings: ', similarity)

if __name__ == "__main__":
  issues = ["Improper use of your report. Incorrect information on your report", "Problem with a credit reporting company's investigation into an existing problem", "Cont'd attempts collect debt not owed"]

  embeddings = []
  for issue in issues:
    sentence = issue
    embedding = sentenceEmbedding(sentence)
    embeddings.append(embedding)
  print(compare_word_embeddings(embeddings[0], embeddings[1]))
  # print(compare_word_embeddings(embeddings[0], embeddings[2]))
  # print(compare_word_embeddings(embeddings[2],embeddings[3]))
