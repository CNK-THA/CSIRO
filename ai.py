# from textgenrnn import textgenrnn
#
# textgen = textgenrnn()

import tensorflow as tf
import numpy as np
import os
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from string import punctuation

sequence_length = 100
BATCH_SIZE = 128
EPOCHS = 30
# dataset file path
FILE_PATH = "C:/Users/s4445655/PycharmProjects/CSIRO/data1"
BASENAME = os.path.basename(FILE_PATH)
# read the data
text = open(FILE_PATH, encoding="utf-8").read()
# remove caps, comment this code if you want uppercase characters as well
text = text.lower()
# remove punctuation
text = text.translate(str.maketrans("", "", punctuation))

# print some stats
n_chars = len(text)
vocab = ''.join(sorted(set(text)))
print("unique_chars:", vocab)
n_unique_chars = len(vocab)
print("Number of characters:", n_chars)
print("Number of unique characters:", n_unique_chars)


# dictionary that converts characters to integers
char2int = {c: i for i, c in enumerate(vocab)}
# dictionary that converts integers to characters
int2char = {i: c for i, c in enumerate(vocab)}

# save these dictionaries for later generation
pickle.dump(char2int, open(f"{BASENAME}-char2int.pickle", "wb"))
pickle.dump(int2char, open(f"{BASENAME}-int2char.pickle", "wb"))


# convert all text into integers
encoded_text = np.array([char2int[c] for c in text])

# construct tf.data.Dataset object
char_dataset = tf.data.Dataset.from_tensor_slices(encoded_text)

# print first 5 characters
for char in char_dataset.take(8):
    print(char.numpy(), int2char[char.numpy()])


# build sequences by batching
sequences = char_dataset.batch(2*sequence_length + 1, drop_remainder=True)

# print sequences
for sequence in sequences.take(2):
    print(''.join([int2char[i] for i in sequence.numpy()]))


def split_sample(sample):
    ds = tf.data.Dataset.from_tensors((sample[:sequence_length], sample[sequence_length]))
    for i in range(1, (len(sample)-1) // 2):
        input_ = sample[i: i+sequence_length]
        target = sample[i+sequence_length]
        # extend the dataset with these samples by concatenate() method
        other_ds = tf.data.Dataset.from_tensors((input_, target))
        ds = ds.concatenate(other_ds)
    return ds

# prepare inputs and targets
dataset = sequences.flat_map(split_sample)


def one_hot_samples(input_, target):
    # onehot encode the inputs and the targets
    return tf.one_hot(input_, n_unique_chars), tf.one_hot(target, n_unique_chars)


dataset = dataset.map(one_hot_samples)

# print first 2 samples
for element in dataset.take(2):
    print("Input:", ''.join([int2char[np.argmax(char_vector)] for char_vector in element[0].numpy()]))
    print("Target:", int2char[np.argmax(element[1].numpy())])
    print("Input shape:", element[0].shape)
    print("Target shape:", element[1].shape)
    print("="*50, "\n")

# https://www.thepythoncode.com/article/text-generation-keras-python



# import numpy
# import sys
# from nltk.tokenize import RegexpTokenizer
# from nltk.corpus import stopwords
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, LSTM
# from keras.utils import np_utils
# from keras.callbacks import ModelCheckpoint
#
#
# file = open("frankenstein-2.txt").read()
#
# def tokenize_words(input):
#     # lowercase everything to standardize it
#     input = input.lower()
#
#     # instantiate the tokenizer
#     tokenizer = RegexpTokenizer(r'\w+')
#     tokens = tokenizer.tokenize(input)
#
#     # if the created token isn't in the stop words, make it part of "filtered"
#     filtered = filter(lambda token: token not in stopwords.words('english'), tokens)
#     return " ".join(filtered)
#
# # preprocess the input data, make tokens
# processed_inputs = tokenize_words(file)
#
# chars = sorted(list(set(processed_inputs)))
# char_to_num = dict((c, i) for i, c in enumerate(chars))
#
# input_len = len(processed_inputs)
# vocab_len = len(chars)
# print ("Total number of characters:", input_len)
# print ("Total vocab:", vocab_len)
#
# seq_length = 100
# x_data = []
# y_data = []
#
# # loop through inputs, start at the beginning and go until we hit
# # the final character we can create a sequence out of
# for i in range(0, input_len - seq_length, 1):
#     # Define input and output sequences
#     # Input is the current character plus desired sequence length
#     in_seq = processed_inputs[i:i + seq_length]
#
#     # Out sequence is the initial character plus total sequence length
#     out_seq = processed_inputs[i + seq_length]
#
#     # We now convert list of characters to integers based on
#     # previously and add the values to our lists
#     x_data.append([char_to_num[char] for char in in_seq])
#     y_data.append(char_to_num[out_seq])
#
# n_patterns = len(x_data)
# print ("Total Patterns:", n_patterns)
#
# X = numpy.reshape(x_data, (n_patterns, seq_length, 1))
# X = X/float(vocab_len)
# y = np_utils.to_categorical(y_data)

# https://stackabuse.com/text-generation-with-python-and-tensorflow-keras/


# import numpy as np
# import pandas as pd
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.utils import np_utils
#
# # text=(open("/Users/pranjal/Desktop/text_generator/sonnets.txt").read())
# # text=text.lower()
#
# characters = sorted(list(set(text)))
# n_to_char = {n:char for n, char in enumerate(characters)}
# char_to_n = {char:n for n, char in enumerate(characters)}
#
# X = []
#  Y = []
# length = len(text)
# seq_length = 100
#   for i in range(0, length-seq_length, 1):
#      sequence = text[i:i + seq_length]
#      label =text[i + seq_length]
#      X.append([char_to_n[char] for char in sequence])
#      Y.append(char_to_n)
#
# X_modified = np.reshape(X, (len(X), seq_length, 1))
# X_modified = X_modified / float(len(characters))
# Y_modified = np_utils.to_categorical(Y)
#
# model = Sequential()
# model.add(LSTM(400, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(400))
# model.add(Dropout(0.2))
# model.add(Dense(Y_modified.shape[1], activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer='adam')
#
# string_mapped = X[99]
# # generating characters
# for i in range(seq_length):
#     x = np.reshape(string_mapped,(1,len(string_mapped), 1))
#     x = x / float(len(characters))
#     pred_index = np.argmax(model.predict(x, verbose=0))
#     seq = [n_to_char[value] for value in string_mapped]
#     string_mapped.append(pred_index)
#     string_mapped = string_mapped[1:len(string_mapped)]
#
# # https://www.analyticsvidhya.com/blog/2018/03/text-generation-using-python-nlp/