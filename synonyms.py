'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math
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
    semantic_descriptors = {}  # Initialize empty dictionary

    for sentence in sentences:
        unique_words = set(sentence)  # Removes duplicate words in a sentence
        for word1 in unique_words:
            if word1 not in semantic_descriptors:
                semantic_descriptors[word1] = {}
            for word2 in unique_words:
                if word1 != word2:  # If the word is not itself, continue
                    if word2 in semantic_descriptors[word1]:
                        semantic_descriptors[word1][word2] += 1  # Increment co-occurrence
                    else:
                        semantic_descriptors[word1][word2] = 1  # Initialize co-occurrence
    return semantic_descriptors

def build_semantic_descriptors_from_files(filenames):
    list_of_sentences = []
    
    for file in filenames:
        with open(file, "r", encoding="latin1") as file:
            text = file.read().lower()

            # Replace specific punctuation with spaces
            for char in '",:;()-–':
                text = text.replace(char, ' ')

            # Replace multiple spaces with a single space
            text = ' '.join(text.split())

            # Split sentences based on `.`, `!`, `?`
            sentences = []
            temp_sentence = []
            for char in text:
                if char in '.!?':
                    if temp_sentence:
                        sentences.append(''.join(temp_sentence).strip())
                        temp_sentence = []
                else:
                    temp_sentence.append(char)
            if temp_sentence:  # Add the last sentence if present
                sentences.append(''.join(temp_sentence).strip())

            # Split each sentence into words and add to the list
            for sentence in sentences:
                words = sentence.split()
                if words:  # Double check if words is not empty
                    list_of_sentences.append(words)

    semantic_descriptors_from_files = build_semantic_descriptors(list_of_sentences)

    return semantic_descriptors_from_files

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = -1
    least_ind = 0
    if word not in semantic_descriptors:
        return choices[0]
    # check if similarity can be computed
    for i in range(len(choices)):
        if choices[i] not in semantic_descriptors:
            similarity = -1
        else:
            #check the semantic similarity
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])

            #check if it xhanges the max value
            if similarity > max_similarity:
                max_similarity = similarity
                least_ind = i

    return choices[least_ind]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    with open(filename, "r", encoding = "latin1") as file:
        questions = file.split("\n")
        for question in questions:
            words = question.split()
            target = words[0]
            answer = words[1]
            choices = words[2:]
            guess = most_similar_word(target, choices, semantic_descriptors, similarity_fn)
            if guess == answer:
                correct+=1
    
        percent_correct = correct/len(questions) * 100
    
    return percent_correct
