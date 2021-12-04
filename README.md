# Information Retrieval System For Boolean Queries 
A search system which can preprocess, build an index for a folder of text data and perform a query processing of free text and phrase queries for information retrieval from Reuters files. Python version 3.8 is used. 

Index is built with: 

python3 index_build.py ./reuters21578/ ./stopwords.txt 


Query processing module is called with:

python3 query_process.py


For query processing please enter a query. Use “w1 w2...wn” for phrase queries, w1 w2...wn for free text queries. Enter E to exit.


P.S:

System may need BS4 library. If so, please run following line on terminal:

python3 -m pip install -r requirements.txt



Implemented by Maral Dicle Maral. November 2021
