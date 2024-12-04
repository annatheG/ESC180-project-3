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

def compute_similarity(wordvec, choices, semantic_descriptors, similarity_fn):
    choice_vec = semantic_descriptors.get(choices, {})
    return similarity_fn(wordvec, choice_vec)

def get_similarity_score(choices, wordvec, semantic_descriptors, similarity_fn): #Helper function to get the similarity score for a specific choice.
    return compute_similarity(wordvec, choices, semantic_descriptors, similarity_fn)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    #returns the choice from choices that is most similar to the given word based on sematic descriptors and similarity function.
    wordvec = semantic_descriptors.get(word)
    if not wordvec:
        return choices[0] #default choice if word is not in descriptors

    best_choice = choices[0]
    best_score = -1000

    for choice in choices:
        score = get_similarity_score(choice, wordvec, semantic_descriptors, similarity_fn)
        if score > best_score:
            best_choice = choice
            best_score = score
    return best_choice

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines() 
    correct = 0 #tracks the amount of correct predictions 
    for line in lines: #goes through all the lines and then splits them 
        parts = line.split()
        if not parts:
            continue 
        word, answer, *choices = parts
        guess = most_similar_word(word, choices, semantic_descriptors, similarity_fn) #this makes a guess with the most similar word function 
        if guess == answer:
            correct += 1
    return (correct / len(lines)) * 100 # calculates the accuracy percentage 
