#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat
from PyDictionary import PyDictionary
import nltk

def get_synonyms(word):
	dictionary = PyDictionary()
	synonyms = dictionary.synonyms(word)

	return synonyms

def open_file():
	user_input = input("Enter file name: ")
	input_string = open(user_input).read()

	return input_string

def write_output(output):
	target_name = input("Enter target name: ")
	target = open(target_name, "w")
	target.write(output)
	target.close()

def get_input_string_sentences(input_string):
	list = input_string.split(".");
	return list

def lower_fk_score(input_string, desired_score):
	sentences = get_sentences(input_string)
	fk_score = textstat.flesch_reading_ease(input_string)

	while fk_score > desired_score:
		for sentence in sentences:
			for word in sentence:
				num_syllables = textstat.syllable_count(word)
				if num_syllables < 3:
					



	return output

def raise_fk_score(input_string, desired_score):
	sentences = get_sentences(input_string)

	return output

def get_stats(input_string):
	num_syllables = textstat.syllable_count(input_string)
	num_words = textstat.lexicon_count(input_string)
	num_sentences = textstat.sentence_count(input_string)
	fk_score = textstat.flesch_reading_ease(input_string)

	print ("Number of words: ", num_words)
	print ("Flesch-Kincaid score: ", fk_score)
	print ("Number of sentences: ", num_sentences)
	print ("Number of syllables: ", num_syllables)

	return num_syllables, num_words, num_sentences, fk_score

def loop():
	input_string = open_file()
	num_syllables, num_words, num_sentences, fk_score = get_stats(input_string)






if __name__ == '__main__':
	loop()
