'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math
from collections import defaultdict # Used in def build_semantic_descriptors
import re # Used in def build_semantic_descriptors_from_files

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as 
    described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    absvec1 = 0
    absvec2 = 0
    dot_product = 0

    for word, count in vec1.items():
        absvec1 += (count)**2
        if word in vec2: # If the word is in the second word's dictionary of co-occurences continue
            dot_product += count * vec2[word]
    for count in vec2.values():
        absvec2 += (count)**2 

    magnitude = math.sqrt(absvec1) * math.sqrt(absvec2)
    if magnitude == 0:
        return 0
    return dot_product / magnitude

def build_semantic_descriptors(sentences):
    semantic_descriptors = defaultdict(lambda: defaultdict(int)) # Makes an empty nested dictionary

    for sentence in sentences:
        unique_words = set(sentence) # Removes duplicate words in a sentence so that we don't double count
        for word1 in unique_words:
            for word2 in unique_words:
                if word1 != word2: # If the word is not itself continue
                    semantic_descriptors[word1][word2] += 1 # Adds one co-occurence to the sub-dictionary

    return semantic_descriptors

def build_semantic_descriptors_from_files(filenames):
    list_of_sentences = []
    
    for file in filenames:
        with open(filenames[file], "r", encoding = "latin1") as file:
            text = file.read().lower()

            text = re.sub(r'[",:;()\-–]', ' ', text) # Removes any unecessary punctuation
            text = re.sub(r'\s+', ' ', text) # Removes any extra spaces

            sentences = re.split(r'[.!?]', text) # Splits the text into sentences based on the three punctuation marks

            for sentence in sentences:
                words = sentence.split()
                if words: # Double checks to see if words is empty
                    list_of_sentences.append(words)

    semantic_descriptors_from_files = build_semantic_descriptors(list_of_sentences)

    return semantic_descriptors_from_files

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

    pass


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    
    pass
