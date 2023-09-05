import random

class Wordle():
    def __init__(self, secretList):
        self._tries = 0
        self._secretWord = random.choice(secretList)
        self._feedback = []

    def setTries(self):        
        self._tries += 1

    def getTries(self):        
        return self._tries

    def getSecretWord(self):        
        return self._secretWord

    def setFeedback(self, guessedWord):
        self._feedback = []
        self.setTries()
        
        stringFeedback = ""
        for letter in self._feedback:
            stringFeedback += letter

        for i in range(5):
            guessedLetter = guessedWord[i]
            if guessedLetter == self._secretWord[i]:
                self._feedback.append("🟩")
            elif guessedLetter in self._secretWord:
                self._feedback.append("🟨")
            else:
                self._feedback.append("🟥")

    def getFeedback(self):
        return self._feedback

    def verify_end_game(self):
        if self._feedback == ['🟩', '🟩', '🟩', '🟩', '🟩']:
            return True
        else:
            return False