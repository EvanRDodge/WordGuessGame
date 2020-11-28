'''
Created on Nov 27, 2020

@author: evand
'''
from tkinter import *
from tkinter import messagebox
import string
from random import randint

root = Tk()
root.title('Word Guess Game')
root.geometry("400x400")

guessCount = 0
secretWords = []
displayedWords = []

def showHelp():
    messagebox.showinfo("How to Play", "You can start a new game by pressing the New Game button.\nThree words will be randomly selected from a list.\nYour goal is to reveal all of the characters in these three words with the fewest number of guesses.\nYou can guess individual characters by pressing the buttons with letters on them.\nYou can also try to guess the whole word by using the text field and guess button on the bottom of the window.\nAll guesses are applied to the currently selected word.\nYou can change which word is currently selected by clicking the circles next to the three words.")

def initializeGame():
    print("initializing game")
    wordFile = open("wordlist.txt", "rt")
    wordCount = 0
    #count lines in file - this is the number of possible words/names
    for line in wordFile:
        wordCount += 1
    #select 3 words/names
    secretWords.clear()
    displayedWords.clear()
    for i in range(0, 3):
        randNum = randint(0, wordCount - 1)
        #find the word/name corresponding to the chosen random number and save it
        wordFile.seek(0)
        index = 0
        while index < randNum:
            index += 1
            wordFile.readline()
        #cut the newline off of the word/name
        secretWords.append(wordFile.readline()[:-1])
        #generate the string to show the player
        tempWord = ""
        for n in range(0, len(secretWords[i])):
            tempWord += "?"
        displayedWords.append(tempWord)
    wordFile.close()
    #update and unlock gui
    global guessCount
    newGameButton.config(state="disabled")
    endGameButton.config(state="normal")
    for i in range(0, 3):
        wordRadios[i].config(text=displayedWords[i], state="normal")
    for btn in letterButtons:
        btn.config(state="normal")
    guessField.config(state="normal")
    guessButton.config(state="normal")
    guessCount = 0
    guessCountLabel.config(text=guessCount)
    print("game initialized")

def concedeGame():
    print("conceding game")
    #reveal hidden words and lock gui
    newGameButton.config(state="normal")
    endGameButton.config(state="disabled")
    for n in range(0, 3):
        wordRadios[n].config(text=secretWords[n], state="disabled")
    for btn in letterButtons:
        btn.config(state="disabled")
    guessField.config(state="disabled")
    guessButton.config(state="disabled")
    print("game conceded")

def guess(ltr):
    print("guessing: " + ltr)
    global guessCount
    global displayedWords
    #search selected word for guessed letter
    for n in range(0, len(secretWords[wordSelection.get()])):
        if ltr == secretWords[wordSelection.get()][n]:
            displayedWords[wordSelection.get()] = displayedWords[wordSelection.get()][:n] + ltr + displayedWords[wordSelection.get()][n+1:]
    #update displayed words
    global wordRadios
    wordRadios[wordSelection.get()].config(text=displayedWords[wordSelection.get()], state="normal")
    guessCount += 1
    guessCountLabel.config(text=guessCount)
    print("guessed: " + ltr)

def guessWholeWord():
    global wordRadios
    global guessCount
    global displayedWords
    #check if the secret word matches the 
    if secretWords[wordSelection.get()] == guessField.get():
        displayedWords[wordSelection.get()] = secretWords[wordSelection.get()]
        wordRadios[wordSelection.get()].config(text=displayedWords[wordSelection.get()])
    guessCount += 1
    guessCountLabel.config(text=guessCount)
    
#define gui widgets
newGameButton = Button(root, text="New Game", padx=5, pady=5, command=initializeGame)
helpButton = Button(root, text="How to Play", padx=5, pady=5, command=showHelp)
endGameButton = Button(root, text="End Game", padx=5, pady=5, state="disabled", command=concedeGame)
frameWords = LabelFrame(root, text="Words & Names",  padx=10, pady=10)
frameGuess = LabelFrame(root, text="Guess", padx=10, pady=10)
selectLabel = Label(frameWords, text="Select a word/name to make guesses toward:")

wordSelection = IntVar()
wordSelection.set(0)
wordRadios = []
wordRadios.append(Radiobutton(frameWords, text="_", variable=wordSelection, value=0, width=50, state="disabled"))
wordRadios.append(Radiobutton(frameWords, text="_", variable=wordSelection, value=1, width=50, state="disabled"))
wordRadios.append(Radiobutton(frameWords, text="_", variable=wordSelection, value=2, width=50, state="disabled"))

letterButtons = []
for letter in "abcdefghijklmnopqrstuvwxyz":
    tempButton = Button(frameGuess, text=letter, width=3, height=2, state="disabled", command=lambda letter=letter : guess(letter))
    letterButtons.append(tempButton)

guessCountLabel = Label(frameGuess, text="0")
guessField = Entry(frameGuess, width=30, borderwidth=3, state="disabled")
guessButton = Button(frameGuess, text="Guess Selected Word/Name", state="disabled", command=guessWholeWord)
#add gui widgets to frames
newGameButton.grid(row=0, column=0)
helpButton.grid(row=0, column=1)
endGameButton.grid(row=0, column=2)
frameWords.grid(row=1, column=0, columnspan=3)
frameGuess.grid(row=2, column=0, columnspan=3)
selectLabel.pack()
for n in range(0, 3):
    wordRadios[n].pack()
for i in range(9):
    for n in range(3):
        if n != 2 or i != 8:
            letterButtons[9*n+i].grid(row=n, column=i, padx=5, pady=5)
guessCountLabel.grid(row=2, column=8, padx=5, pady=5)
guessField.grid(row=3, column=0, columnspan=5, padx=5, pady=5)
guessButton.grid(row=3, column=5, columnspan=4, padx=5, pady=5)

root.mainloop()