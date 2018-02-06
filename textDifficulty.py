#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat

if __name__ == '__main__':

	userInput = raw_input("Enter file name: ")
	inputString = open(userInput).read()

	print "Number of words: ", textstat.lexicon_count(inputString)		
	print "Flesch-Kincaid score: ", textstat.flesch_reading_ease(inputString)
	
