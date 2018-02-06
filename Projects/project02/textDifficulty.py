#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat

if __name__ == '__main__':

	user_input = input("Enter file name: ")
	input_string = open(userInput).read()

	num_words = textstat.lexicon_count(inputString)
	fk_score = textstat.flesch_reading_ease(inputString)

	print ("Number of words: ", num_words)
	print ("Flesch-Kincaid score: ", fk_score)
