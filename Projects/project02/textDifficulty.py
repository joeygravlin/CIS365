#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

def get_new_string(input_string, copy_string):
	# loop through each token (word, comma, period) in the input file
	for word in word_tokenize(input_string):
		# find a set of synonyms for each word
		synonym_set = wordnet.synsets(word)
		# if there is a synonym for that word
		if synonym_set:
			# get just the first synonym
			first_synonym = synonym_set[0].lemmas()[0].name()
			# if the synonym has less syllabes than the word
			if textstat.syllable_count(first_synonym) < textstat.syllable_count(word):
				words_with_synonyms.append(word)
				the_synonyms.append(first_synonym)

	# replace all the words with their corresponding synonyms
	i = 0
	while i < len(words_with_synonyms):
		copy_string = [w.replace(words_with_synonyms[i], the_synonyms[i]) for w in copy_string]
		i += 1
	# join the list into one string
	FINAL_STRING = " ".join(copy_string)
	return FINAL_STRING


if __name__ == '__main__':

	# prompt user for file and open it
	user_input = input ("Enter file name: ")
	input_string = open (user_input).read()

	# declare/initialize lists
	copy_string = input_string.split()
	words_with_synonyms = []
	the_synonyms = []

	# get number of syllables, words, sentences, and FK score for the file
	num_syllables = textstat.syllable_count(input_string)
	num_words = textstat.lexicon_count(input_string)
	num_sentences = textstat.sentence_count(input_string)
	fk_score = textstat.flesch_reading_ease(input_string)

	# print number of syllables, words, and sentences in the file
	print ("\nNumber of syllables: ", num_syllables)
	print ("Number of words: ", num_words)
	print ("Number of sentences: ", num_sentences)

	output = get_new_string(input_string, copy_string)

	# print the original text and the new text with their FK scores
	print ("\n\nOriginal text: ", input_string)
	print ("Flesch-Kincaid score: ", fk_score)
	print ("\n\nNew text: ", output)
	print ("\nNew Flesch-Kincaid score: ", textstat.flesch_reading_ease(output))
	print ("\n")
