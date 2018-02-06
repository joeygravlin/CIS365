#
# Alex Duncanson, Derrik Fleming, Gary Fleming, Joseph Gravlin
#
from textstat.textstat import textstat

userInput = raw_input("Enter Filename: ")

with open(userInput) as IF:
	print textstat.flesch_reading_ease(IF.read())
