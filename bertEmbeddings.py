# API to generate word embeddings

#
import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine

def generate_tensors(sentences, tokenizer):
    input_ids = []
    segments = []
    # For every sentence...
    for sent in sentences:
        sent = sentences
        max_length = len(tokenizer.tokenize(sent))
        encoded_dict = tokenizer.encode_plus(
            sent,  # Sentence to encode.
            add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
            max_length=max_length,  # Pad & truncate all sentences.
            pad_to_max_length=True,
            return_attention_mask=True,  # Construct attn. masks.
            return_tensors='pt',  # Return pytorch tensors.
        )

        # Add the encoded sentence to the list.
        input_ids.append(encoded_dict['input_ids'])

        # Mark each of the tokens as belonging to sentence "1".
        segments_ids = [1] * max_length

    # Convert the lists into tensors.
    input_tensors = torch.cat(input_ids, dim=0)
    segments_tensors = torch.tensor([segments_ids])

    return input_tensors, segments_tensors

# Load pre-trained model (weights)
def load_pretrained_bert_model():
  model = BertModel.from_pretrained('bert-base-uncased',
                                  output_hidden_states = True, # Whether the model returns all hidden-states.
                                  )

  # Put the model in "evaluation" mode, meaning feed-forward operation.
  model.eval()

  return model

# Run the text through BERT, and collect all of the hidden states produced
# from all 12 layers.
def run_model(model, input_tensors, segment_tensors):
  with torch.no_grad():
    outputs = model(input_tensors, segment_tensors)
    states = outputs.hidden_states
  return states

def compute_mean_last4_states(states):
  layers = [-4, -3, -2, -1]
  output = torch.stack([states[i] for i in layers]).sum(0).squeeze()
  #output = torch.stack(states, dim=0)  --> differs from top line

  word_embedding =  output.mean(dim=0)
  return word_embedding

def generate_word_embeddings(sentence):
    # Load pre-trained model tokenizer (vocabulary)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # tokenize sentence & build tensors
    input_tensors, segment_tensors = generate_tensors(sentence, tokenizer)

    # load pre-trained bert model
    model = load_pretrained_bert_model()

    # run model
    states = run_model(model, input_tensors, segment_tensors)

    # compute word embeddings
    word_embeddings = compute_mean_last4_states(states)

    return word_embeddings

def compare_word_embeddings(embedding1, embedding2):
    similarity = 1 - cosine(embedding1, embedding2)
    print('Similarity between the 2 embeddings: ', similarity)


if __name__ == "__main__":
  sentence = "After stealing money from the bank vault, the bank robber was seen fishing on the Mississippi river bank."
  word_embeddings = generate_word_embeddings(sentence)
  # validate
  bank_vault = word_embeddings[5]
  bank_robber = word_embeddings[9]
  compare_word_embeddings(bank_vault, bank_robber)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
