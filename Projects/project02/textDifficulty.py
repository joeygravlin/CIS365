#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

#obsolete, not effective
def remove_adjective(input_string, copy_string):
	word_list = word_tokenize(input_string)
	dict = nltk.tag.pos_tag(word_list)
	symbol_list = [",", ".", ";", "--", "&", "$", "#", "@", "!", ":", "*", "'"]
	FINAL_STRING = ""
	for word in dict:
		if FINAL_STRING == "" or word[0] in symbol_list:
			FINAL_STRING += word[0]
		elif FINAL_STRING != "" and (word[1] != 'JJ' or word[1] != 'JJR' or word[1] != 'JJS'):
			FINAL_STRING += " " + word[0]

	print("FINAL:  \n" + FINAL_STRING)

	return FINAL_STRING

def find_lowest_syl_count(syn_list):
	#12 is largest number of syllables in one english word
	lowest_count = 12
	lowest_count_word = ""

	for synset in syn_list:
		word = synset.name().split('.')[0]
		count = textstat.syllable_count(word)

		if count < lowest_count:
			lowest_count = count
			lowest_count_word = word

	return lowest_count_word


def get_new_string(input_string, copy_string):
	# loop through each token (word, comma, period) in the input file
	for word in word_tokenize(input_string):
		# find a set of synonyms for each word
		synonym_set = wordnet.synsets(word)
		# if there is a synonym for that word
		if synonym_set:
			#get the synonym with the lowest syllable count
			synonym = find_lowest_syl_count(synonym_set)

			# get just the first synonym
			#synonym = synonym_set[0].lemmas()[0].name()

			# if the synonym has less syllabes than the word
			if textstat.syllable_count(synonym) < textstat.syllable_count(word):
				words_with_synonyms.append(word)
				#view synonym changes
				#print(word, "-->", synonym, "\n")
				the_synonyms.append(synonym)

	# replace all the words with their corresponding synonyms
	i = 0
	while i < len(words_with_synonyms):
		copy_string = [w.replace(words_with_synonyms[i], the_synonyms[i]) for w in copy_string]
		i += 1

	# join the list into one string
	FINAL_STRING = " ".join(copy_string)
	return FINAL_STRING

def check_reading_level(input_string):
	level = ["college graduate","college","12th grade","11th grade","10th grade","9th grade","8th grade","7th grade","6th grade","5th grade"]
	grade = []
	if textstat.flesch_kincaid_grade(input_string) <= 5:
		grade.append(level[9])
	elif textstat.flesch_kincaid_grade(input_string) <= 6:
		grade.append(level[8])
	elif textstat.flesch_kincaid_grade(input_string) <= 7:
		grade.append(level[7])
	elif textstat.flesch_kincaid_grade(input_string) <= 8:
		grade.append(level[6])
	elif textstat.flesch_kincaid_grade(input_string) <= 9:
		grade.append(level[5])
	elif textstat.flesch_kincaid_grade(input_string) <= 10:
		grade.append(level[4])
	elif textstat.flesch_kincaid_grade(input_string) <= 11:
		grade.append(level[3])
	elif textstat.flesch_kincaid_grade(input_string) <= 12:
		grade.append(level[2])
	elif textstat.flesch_kincaid_grade(input_string) <= 13:
		grade.append(level[1])
	else:
		grade.append(level[0])

	grade_string = " ".join(grade)
	return grade_string

if __name__ == '__main__':

	# prompt user for file and open it
	user_input = input ("Enter file name to open: ")
	input_string = open(user_input).read()
	user_input = input ("Enter file name to write to: ")


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
	for i in range(0,5):
		output = get_new_string(output, copy_string)
	#output = remove_adjective(output, copy_string)
	initial_grade = check_reading_level(input_string)
	new_grade = check_reading_level(output)

	#write new text to file
	with open(user_input, "w") as text_file:
		print(output, file=text_file)

	# print the original text and the new text with their FK scores
	#print ("\n\nOriginal text: ", input_string)
	print ("Flesch-Kincaid score: ", fk_score)
	print(initial_grade, "reading level")
	#print ("\n\nNew text: ", output)
	print ("\nNew Flesch-Kincaid score: ", textstat.flesch_reading_ease(output))
	print(new_grade, "reading level")
	print ("\n")
