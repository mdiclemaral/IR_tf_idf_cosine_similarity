# “fourth quarter performance”
# “James Baker”

"""

Query Processing and Search. Works with: python3 query_process.py
Please enter a query (Use “w1 w2...wn” for phrase queries, w1 w2...wn for free text queries). Enter E to exit.

Reads the index.pkl and idf_index.pkl files as the index. Contains conjuction_phrase(), position_process(),
conjuction_free(), cosine_similarity(), query_tdf_idf(), free_text_process(), phrase_process()
and query_process() functions.

"""
import math
import pickle
import time
import sys


"""
Conjunction function for phrase queries. Processes the conjunction operation for search words while calling the 
position_process() function for positional identification of the queries.

"""

def conjunction_phrase (doc1, doc2):

    i,j = 0,0
    cach = {}

    keys1 = sorted(doc1.keys())
    keys2 = sorted(doc2.keys())

    while i < len(keys2) and j < len(keys1):

        if keys2[i] == keys1[j]:

            position_cach = position_process(doc1[keys1[j]], doc2[keys2[i]])
            if not len(position_cach) == 0:
                cach[keys1[j]] = position_cach
            j += 1
            i += 1
        elif keys2[i] > keys1[j]:
            j += 1
        else:
            i += 1

    return cach

"""
Conjunction function for positions of the query words. Processes the conjunction operationfor positional identification 
of the queries.

"""
def position_process(d1, d2):

    i,j = 0,0
    result = []
    while i < len(d1) and j < len(d2):
        if (d1[i] + 1) == d2[j]:
            result.append(d1[i]+1)
            j += 1
            i += 1
        elif d1[i] > d2[j]:
            j += 1
        else:
            i += 1
    return(result)

"""
Computes the cosine similarity for two given vectors.

"""
def cosine_similarity(vec1, vec2):

    dot = 0.0
    norm_vec1 = 0
    norm_vec2 = 0
    for v in range(0, len(vec1)):
        temp_dot = (vec1[v] * vec2[v])
        dot += temp_dot
        norm_vec1 += vec1[v] * vec1[v]
        norm_vec2 += vec2[v] * vec2[v]
    norm_vec1 = math.sqrt(norm_vec1)
    norm_vec2 = math.sqrt(norm_vec2)

    cos_sim = dot / (norm_vec1 * norm_vec2)

    return cos_sim

"""
Computes tf_idf values for entered queries.

"""
def query_tdf_idf(query_list, idf_index):
    query_dict = {}
    query_tf_idf_list = []

    for word in query_list:
        if not word in query_dict:
            query_dict[word] = 1
        else:
            query_dict[word] += 1

    for word in query_list:
        total_words = len(query_list)
        tf = 1 + math.log(query_dict[word],10)#/total_words, 10)
        idf = idf_index[word]
        w = tf * idf
        query_tf_idf_list.append(w)

    return query_tf_idf_list

"""
Conjunction function for free text queries. Processes the conjunction operation for two given lists.

"""
def conjunction_free (doc1, doc2):

    i, j = 0, 0
    cach = []
    if len(doc1) <= len(doc2):
        doc_long = doc2
        doc_short = doc1
    else:
        doc_long = doc1
        doc_short = doc2

    while i < len(doc_long) and j < len(doc_short):
        if doc_long[i] == doc_short[j]:
            cach.append(doc_long[i])
            j += 1
            i += 1
        elif doc_long[i] > doc_short[j]:
            j += 1
        else:
            i += 1

    return cach
"""
Process function for free text queries. Processes the conjunction_free() operation for the queries, computes tf_idf values 
for queries with query_tdf_idf() function and computes the cosine similarities between query and the documents 
with cosine_similarity() function. 

"""

def free_text_process(query_list, tdf_idf_index, idf_index):

    word_list = []

    for word in query_list:
        temp_list = list(tdf_idf_index[word].keys())
        temp_list.sort()
        word_list.append(temp_list)

    word_count = 1
    op_cach = word_list[0]

    if not len(word_list) == 1:
        for op in range(len(word_list)-1):
            op_cach = conjunction_free(op_cach, word_list[word_count])
            word_count += 1

    doc_tf_idf_list = {}
    for doc in op_cach:
        tf_idf_for_query_words = []
        for word in query_list:
            tf_idf_for_query_words.append(tdf_idf_index[word][doc])
        doc_tf_idf_list[doc] = (tf_idf_for_query_words)
    query_tdf_idf_list = query_tdf_idf(query_list, idf_index)

    cos_sim = {}
    for doc in doc_tf_idf_list:

        sim_score = cosine_similarity(query_tdf_idf_list, doc_tf_idf_list[doc])
        cos_sim[doc] = sim_score

    ordered_sim = sorted(cos_sim.items(), key=lambda x: x[1], reverse=True) #Sort by similarity

    return ordered_sim


"""
Process function for phrase queries. Processes the conjunction_phrase() operation for the query and the documents, 
finds the documents with the given phrase query. 

"""
def phrase_process(query_list, index):

    word_list = []
    for word in query_list:
        word_list.append(index[word])

    word_count = 1
    op_cach = word_list[0]

    if not len(word_list) == 1:
        for op in range(len(word_list)-1):
            op_cach = conjunction_phrase(op_cach, word_list[word_count])
            word_count += 1
    result = sorted(list(op_cach.keys()))
    return result

"""

Processes queries into machine readable form and performs phrase_process() and free_text_process() operations
for search words entered by the user.

"""
def query_process(query, index, tdf_idf_index, idf_index):

    #Finds the phrase queries.
    phrase = False
    if query.startswith('"'):
        phrase = True

    # Cleans punctuations.
    punct = '''“”!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~'''
    for t in query:
        if t in punct:
            query = query.replace(t, " ")

    query = query.lower()
    query_list = query.strip().split()

    # Remove words that are not in the indices.
    for word in query_list:

        if word not in index:
            return []

    # Calls phrase and free text query functions.
    if phrase:
        merge_result = phrase_process(query_list, index)
    else:
        merge_result = free_text_process(query_list, tdf_idf_index, idf_index)

    return merge_result

def main():

    try:
        idx_file = open("index.pkl", "rb")
        index = pickle.load(idx_file)
        idx_file2 = open("tdf_idf_index.pkl", "rb")
        tdf_idf_index = pickle.load(idx_file2)
        idx_file3 = open("idf_index.pkl", "rb")
        idf_index = pickle.load(idx_file3)
        print('Index is succesfully loaded!')
    except(FileNotFoundError):
        index = None
        tdf_idf_index = None
        idf_index = None
        print('INDEX IS NOT CREATED. Please first run the following command to create an index file:')
        print('python3 index_build.py folder_directory stop_words_directory')
        exit(0)

    print('Please enter a query (Use “w1 w2...wn” for phrase queries, w1 w2...wn for free text queries.). Enter ''E'' to exit.')

    while True:
        query = input("Please enter a query(''E'' for exit):")
        if query == 'E':
            print('Thank you for using my search engine!')
            break
        start_time = time.time()
        result = query_process(query, index, tdf_idf_index, idf_index)
        end_time = time.time()
        run_time = end_time - start_time
        round(run_time, 3)
        if len(result) == 0:
            print(query + '  is not found.')
        else:
            print(query + ' is found at: ')
            print(result)
        print("- Process finished in %.6f seconds -" % run_time)



if __name__ == '__main__':

    main()