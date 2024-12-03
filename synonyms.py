'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math


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
        if word in vec2:
            dot_product += count * vec2[word]
    for count in vec2.values():
        absvec2 += (count)**2 

    magnitude = math.sqrt(absvec1) * math.sqrt(absvec2)
    if magnitude == 0:
        return 0
    return dot_product / magnitude

def build_semantic_descriptors(sentences):
    pass

def build_semantic_descriptors_from_files(filenames):
    pass



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    pass


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    pass
