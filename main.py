import streamlit as st 
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize
import glob
import re
import os
import numpy as np
import sys

Stopwords = set(stopwords.words('english'))
# nltk.download()

# st.title("EEE")
# st.subheader("Eagle Eye Engin")
def search():
    exsit = True 

    def finding_all_unique_words_and_freq(words):
        words_unique = []
        word_freq = {}
        for word in words:
            if word not in words_unique:
                words_unique.append(word)
        for word in words_unique:
            word_freq[word] = words.count(word)
        return word_freq
    def finding_freq_of_word_in_doc(word,words):
        freq = words.count(word)
            
    def remove_special_characters(text):
        regex = re.compile('[^a-zA-Z0-9\s]')
        text_returned = re.sub(regex,'',text)
        return text_returned

    class Node:
        def __init__(self ,docId, freq = None):
            self.freq = freq
            self.doc = docId
            self.nextval = None
        
    class SlinkedList:
        def __init__(self ,head = None):
            self.head = head

    all_words = []
    dict_global = {}
    file_folder = 'data/*'
    idx = 1
    files_with_index = {}
    for file in glob.glob(file_folder):
        print(file)
        fname = file
        file = open(file , "r")
        text = file.read()
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'),'',text)
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [word for word in words if len(words)>1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        dict_global.update(finding_all_unique_words_and_freq(words))
        files_with_index[idx] = os.path.basename(fname)
        idx = idx + 1
        
    unique_words_all = set(dict_global.keys())

    linked_list_data = {}
    for word in unique_words_all:
        linked_list_data[word] = SlinkedList()
        linked_list_data[word].head = Node(1,Node)

    word_freq_in_doc = {}
    idx = 1
    for file in glob.glob(file_folder):
        file = open(file, "r")
        text = file.read()
        text = remove_special_characters(text)
        text = re.sub(re.compile('\d'),'',text)
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        words = [word for word in words if len(words)>1]
        words = [word.lower() for word in words]
        words = [word for word in words if word not in Stopwords]
        word_freq_in_doc = finding_all_unique_words_and_freq(words)
        for word in word_freq_in_doc.keys():
            linked_list = linked_list_data[word].head
            while linked_list.nextval is not None:
                linked_list = linked_list.nextval
            linked_list.nextval = Node(idx ,word_freq_in_doc[word])
        idx = idx + 1


    query = st.text_input('Enter your query:', max_chars=150)
    go = st.button('GO')

    if go:
        query = word_tokenize(query)
        cnt = 1
        connecting_words = []
        different_words = []
        for word in query:
            if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
                different_words.append(word.lower())
            else:
                connecting_words.append(word.lower())
        st.write('The connecting words are: ',connecting_words)
        total_files = len(files_with_index)
        zeroes_and_ones = []
        zeroes_and_ones_of_all_words = []
        for word in (different_words):

            if word.lower() in unique_words_all:
                zeroes_and_ones = [0] * total_files
                linkedlist = linked_list_data[word].head
                print(word)
                while linkedlist.nextval is not None:
                    zeroes_and_ones[linkedlist.nextval.doc - 1] = 1
                    linkedlist = linkedlist.nextval
                zeroes_and_ones_of_all_words.append(zeroes_and_ones)

            else:
                st.write(word," not found")
                exsit = False
                # sys.exit()
        print(zeroes_and_ones_of_all_words)
        
        for word in connecting_words:
            word_list1 = zeroes_and_ones_of_all_words[0]
            word_list2 = zeroes_and_ones_of_all_words[1]
            if word == "and":
                bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,word_list2)]
                zeroes_and_ones_of_all_words.remove(word_list1)
                zeroes_and_ones_of_all_words.remove(word_list2)
                zeroes_and_ones_of_all_words.insert(0, bitwise_op);
            elif word == "or":
                bitwise_op = [w1 | w2 for (w1,w2) in zip(word_list1,word_list2)]
                zeroes_and_ones_of_all_words.remove(word_list1)
                zeroes_and_ones_of_all_words.remove(word_list2)
                zeroes_and_ones_of_all_words.insert(0, bitwise_op);
            elif word == "not":
                bitwise_op = [not w1 for w1 in word_list2]
                bitwise_op = [int(b == True) for b in bitwise_op]
                zeroes_and_ones_of_all_words.remove(word_list2)
                zeroes_and_ones_of_all_words.remove(word_list1)
                bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,bitwise_op)]
                zeroes_and_ones_of_all_words.insert(0, bitwise_op);
                
        files = []    
        lis = zeroes_and_ones_of_all_words
        cnt = 1
        for index in lis:
            if index == 1:
                files.append(files_with_index[cnt])
            cnt = cnt+1

        if exsit == True:
            all_files = [] 
            for file in glob.glob(file_folder):
                all_files.append(file)

            print(all_files)
                
            result = []

            for x in range(len(lis[0])):
                if lis[0][x] == 1:
                    result.append(all_files[x])

            print(result)

            st.write("Resut Files",result)
            print("--------------------")
        else:
            st.write("Try something else")

        
            print("--------------------")

def func():
    st.title("Short description on how EEE works!")
    st.text("1 - EEE loops around all the files and finds all the uniqe words excluding any connecting word \n" +
    "2 - EEE creates a linkedlist for each unique word.\n" +
    "3 - Now each word has a linkedlist. So, EEE appends the files containing the word into the linkedlist"+
    " along with the frequency\n"+
    "4 - The user enters his query -> EEE process the query and seperats the connecting words (AND, OR, NOT)"+
    "from the different words\n"+
    "5 - Finally EEE perform the search algorithm on defferent words considering the connecting words"+
    " and returns the output")
    st.image("algo_desc.png")
def main():
    st.sidebar.title("EEE")
    st.sidebar.image("logo11.png")
    st.image("logo22.png")

    selected_box = st.sidebar.selectbox(
        'Navigator',
        ('Search','How It Works?' )
        )

    st.sidebar.write("  ")
    st.sidebar.write("  ")
    st.sidebar.write("  ")
    st.sidebar.write("  ")
    st.sidebar.write("  ")
    st.sidebar.checkbox("Safe Search")
    st.sidebar.checkbox("Kids Mode")

    if selected_box == 'How It Works?':
        func() 
    if selected_box == 'Search':
        search()


if __name__ == "__main__":
    main()
