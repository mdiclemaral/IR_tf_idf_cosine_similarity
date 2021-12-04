"""
Indexing file. Works with: python3 index_build.py folder_directory stop_words_directory
Drops a index.pkl, idf_index.pkl and tdf_idf_index.pkl files to the current directory.
Contains compute_tf(), compute_idf(), processor(), indxer(), fileHandler() functions.

"""

from bs4 import BeautifulSoup
import os
import time
from multiprocessing import Process, Manager
import pickle
import math
import sys
import string
start_time = time.time()

#'sasco': {12169: [15, 22]}

"""
Computes term frequencies for the words in the created inverted index file, calls compute_idf() function to calculate
idf values for index terms and finally enters the tf_idf values of the words into tf_idf_index.pkl

"""

def compute_tf(index, num_words_in_docs):
    idf_index = compute_idf(index, num_words_in_docs)
    tf_idf_index = {}
    for word in index:
        doc_tf= {}
        for doc in index[word]:
           tf = len(index[word][doc])# / int(num_words_in_docs[doc])
           tf_idf = (1 + math.log(tf, 10)) * idf_index[word]
           doc_tf[doc] = tf_idf
        tf_idf_index[word] = doc_tf
    #print(tf_idf_index)
    return tf_idf_index

"""
Computes the document frequencies for the words in the created inverted index file, enters the 
idf weights of the words into idf_index.pkl

"""
def compute_idf(index, num_words_in_docs):
    total_docs = max(list(num_words_in_docs.keys()))
    idf_idx = {}
    for word in index:
        idf_idx[word] = math.log((total_docs/len(index[word])), 10)

    idx_dump_idf = open("idf_index.pkl", "wb")
    pickle.dump(idf_idx, idx_dump_idf)
    idx_dump_idf.close()
    #print(idf_idx)
    return idf_idx

"""
Reads an individual file and the stop_words file, tokenizes, cleans stop words and punctuations of the docs. 
Changes result to a list of tokenized words. 

"""

def processor(dir, stops, input, result):

    stop_words = open(stops).read().split()
    punct = string.punctuation
    #punct = '''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~''' #From string.punctuation list

    file_handler = open(dir + input, 'r', encoding='latin1').read()
    soup = BeautifulSoup(file_handler, 'html.parser')

    reuters = soup.find_all('reuters')

    #Reads reuters documents, tokenizes, cleans stop words and punctuations
    for r in reuters:
        id = r['newid']
        if r.body == None:
            result[id] = []
            continue
        text = r.text.lower()
        for t in text:
            if t in punct:
                text = text.replace(t, " ")

        text = text.replace('\n', ' ')
        tokens = text.replace('\t', ' ')

        tokenized = tokens.split()
        tokenized1 = []
        for t in tokenized:
            if not t in stop_words:
                tokenized1.append(t)

        result[id] = tokenized1

"""

Builds the inverted index and saves the inverted index dictionary as a file.

"""
def idxer(docs):

    num_words_in_docs = {}
    inverted_idx = {}
    for key in docs:
        ID = int(key)
        words = docs[key]
        num_words_in_docs[ID] = len(words)
        for num_word in range(0, len(words)):
            word = words[num_word]

            if not word in inverted_idx:
                position_dict = {}
                position_dict[ID] = [num_word]
                inverted_idx[word] = position_dict
            else:
                if ID in inverted_idx[word]:# If docID is already added to the inverted index, continue
                    inverted_idx[word][ID].append(num_word)
                else:
                    inverted_idx[word][ID] = [num_word]
    tf_idf_idx = compute_tf(inverted_idx, num_words_in_docs)


    #Saves the inverted index into current file.
    idx_dump = open("index.pkl", "wb")
    pickle.dump(inverted_idx, idx_dump)
    idx_dump.close()
    idx_dump_tf = open("tdf_idf_index.pkl", "wb")
    pickle.dump(tf_idf_idx, idx_dump_tf)
    idx_dump_tf.close()

    #print(inverted_idx)
    return inverted_idx

"""

Creates a new process for each file in reuters directory calls processor() for each file. 
A common dictionary for ID: words is kept for processes.
idxer() is called to create word: IDs 

"""
def fileHandler(dir, stops):
    files = os.listdir(dir)
    input_starter = 'reut'
    manager = Manager()
    w_dict = manager.dict()
    processes = []
    results = []
    count = 0

    for f in files:
        if input_starter in f:
            temp_dict = {}
            process = Process(target=processor, args=(dir, stops, f, w_dict))
            results.append(temp_dict)
            processes.append(process)
            process.start()
            count += 1
    for i in range(len(processes)):
        processes[i].join()

    idxer(w_dict)


def main():
    stops = sys.argv[2]
    dir = sys.argv[1]
    fileHandler(dir,stops)


if __name__ == '__main__':
    main()
    run_time = time.time() - start_time
    print("- Index is created in %.6f seconds -" % (round(run_time, 5)))
    #print("- Index is created in %s seconds -" % (time.time() - start_time))

