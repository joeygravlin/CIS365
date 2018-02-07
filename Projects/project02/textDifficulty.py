#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

if __name__ == '__main__':

	user_input = input("Enter file name: ")
	input_string = open(user_input).read()
	new_string = ""

	num_syllables = textstat.syllable_count(input_string)
	num_words = textstat.lexicon_count(input_string)
	num_sentences = textstat.sentence_count(input_string)
	fk_score = textstat.flesch_reading_ease(input_string)

	print ("Number of syllables: ", num_syllables)
	print ("Number of words: ", num_words)
	print ("Number of sentences: ", num_sentences)
	print ("Flesch-Kincaid score: ", fk_score)

	for word in word_tokenize(input_string):
		synonym_set = wordnet.synsets(word.strip("."))
		first_synonym = synonym_set[0].lemmas()[0].name()

		if first_synonym:
			print (word, "or", first_synonym)
			if textstat.syllable_count(first_synonym) < textstat.syllable_count(word):
				#input_string.replace(word, first_synonym, inf)
				new_string += " " + first_synonym
			else:
				new_string += " " +  word

	print("\n\nOriginal text: ", input_string)
	print("\n\nNew text: ", new_string)
