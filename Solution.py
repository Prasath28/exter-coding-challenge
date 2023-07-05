import csv
import time
import psutil

def load_dictionary(dictionary_file):
    """
    Load the English to French dictionary from the CSV file.
    Returns a dictionary object.
    """
    dictionary = {}
    with open(dictionary_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                english_word = row[0]
                french_word = row[1]
                dictionary[english_word] = french_word
    return dictionary

def load_find_words(find_words_file):
    """
    Load the find words list from the text file.
    Returns a list of words.
    """
    with open(find_words_file, 'r', encoding='utf-8') as file:
        find_words = file.read().splitlines()
    return find_words

def replace_words(text, dictionary, find_words):
    """
    Replace the English words in the text with their French counterparts.
    Returns the modified text and a dictionary of replaced words.
    """
    replaced_words = {}
    modified_text = text
    for word in find_words:
        if word.lower() in dictionary:
            french_word = dictionary[word.lower()]
            modified_text = modified_text.replace(word, french_word)
            replaced_words[word] = french_word
    return modified_text, replaced_words

def process_text(input_file, find_words_file, dictionary_file):
    """
    Process the input text file and replace English words with French words.
    Returns the modified text, replaced word count, processing time, and memory usage.
    """
    start_time = time.time()

    # Load dictionary and find words list
    dictionary = load_dictionary(dictionary_file)
    find_words = load_find_words(find_words_file)

    # Read input text file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Replace words
    modified_text, replaced_words = replace_words(text, dictionary, find_words)

    end_time = time.time()
    processing_time = end_time - start_time
    memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # in MB

    return modified_text, replaced_words, len(replaced_words), processing_time, memory_usage

# File paths
input_file = 't8.shakespeare.txt'
find_words_file = 'find_words.txt'
dictionary_file = 'french_dictionary.csv'

# Process the text
modified_text, replaced_words, replaced_word_count, processing_time, memory_usage = process_text(
    input_file, find_words_file, dictionary_file)

# Save the output
output_file = 't8.shakespeare.translated.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(modified_text)

# Write performance information to performance.txt
performance_file = 'performance.txt'
with open(performance_file, 'w', encoding='utf-8') as file:
    file.write(f"Time to process: {processing_time / 60:.0f} minutes {processing_time % 60:.0f} seconds\n")
    file.write(f"Memory used: {memory_usage:.2f} MB")

#Count the frequency of replaced words
word_frequency = {}
for word in replaced_words:
    french_word = replaced_words[word]
    if french_word in word_frequency:
        word_frequency[french_word] += 1
    else:
        word_frequency[french_word] = 1

# Write frequency information to frequency.csv
frequency_file = 'frequency.csv'
with open(frequency_file, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['English word', 'French word', 'Frequency'])
    for word in replaced_words:
        english_word = word
        french_word = replaced_words[word]
        frequency = word_frequency[french_word]
        writer.writerow([english_word, french_word, frequency])

