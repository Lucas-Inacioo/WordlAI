from collections import Counter
from operator import itemgetter
import random

class Player():
    def __init__(self, wordList, wordle_match):
        self._letters = []
        self._wrongLetters = set()
        self._knownLettersPositions = set()
        self._correctLetter = ["", "", "", "", ""]
        self._allInputs = []
        self._wordList = wordList
        self._result = 0
        self._wordle_match = wordle_match
    
    def getAllInputs(self):
        return self._allInputs
    
    def getResult(self):
        return self._result

    def play(self):
        self.letter_counter(self._wordList)
        inputWord = random.choice(self.filter_best(self._wordList))
        self._allInputs.append(inputWord)
        self._secretWord = self._wordle_match.getSecretWord
        self._wordle_match.setFeedback(inputWord)
        
        if self._wordle_match.verify_end_game():
            self._result = 1
            return
        else:
            while self._wordle_match.getTries() < 6:
                inputWord = self.ai(self._wordList, self._wordle_match, self._allInputs)    
                self._allInputs.append(inputWord)
                self._wordle_match.setFeedback(inputWord)
                if self._wordle_match.verify_end_game():
                    self._result = 1
                    return
    
    def ai(self, possible_guesses, wordle_match, allInputs):
        self.analyze_feedback(wordle_match, allInputs)

        if (wordle_match.getTries() < 3):
            most_yellows_filtered = self.filter_red(possible_guesses)
            most_yellows_filtered = self.filter_most_yellows(most_yellows_filtered)
            if len(most_yellows_filtered) > 0:
                possible_guesses = most_yellows_filtered
            else:
                possible_guesses = self.filter_green(possible_guesses)
                possible_guesses = self.filter_red(possible_guesses)
                possible_guesses = self.filter_yellow(possible_guesses)
        else:
            possible_guesses = self.filter_green(possible_guesses)
            possible_guesses = self.filter_red(possible_guesses)
            possible_guesses = self.filter_yellow(possible_guesses)
            
        possible_guesses = self.filter_best(possible_guesses)
        best_guess = random.choice(possible_guesses)     
        return best_guess

    def filter_most_yellows(self, possible_guesses):
        filtered_guesses = []
        for guess in possible_guesses:
            match = True
            for i in range(5):
                if self._correctLetter[i] != "" and self._correctLetter[i] == guess[i]:
                    match = False
                    break
            for pair in self._knownLettersPositions:
                if pair[0] in guess:
                    match = False
                    break
            if match == True:
                filtered_guesses.append(guess)
        return filtered_guesses

    def analyze_feedback(self, wordle_match, allInputs):
        lastInput = allInputs[-1]
        for i in range(5):
            feedback = wordle_match.getFeedback()
            if feedback[i] == "🟩":
                self._correctLetter[i] = lastInput[i]
                self._knownLettersPositions.add((lastInput[i], None))
            elif feedback[i] == "🟨":
                self._knownLettersPositions.add((lastInput[i], i))
            elif feedback[i] == "🟥":
                if lastInput[i] in self._letters:
                    self._letters.remove(lastInput[i])
                self._wrongLetters.add(lastInput[i])

    def filter_green(self, possible_guesses):
        filtered_guesses = []
        for guess in possible_guesses:
            match = True
            for i in range(5):
                if self._correctLetter[i] != "" and self._correctLetter[i] != guess[i]:
                    match = False
                    break
            if match == True:
                filtered_guesses.append(guess)

        return filtered_guesses

    def filter_yellow(self, possible_guesses):
        filtered_guesses = []
        for guess in possible_guesses:
            match = True
            for pair in self._knownLettersPositions:
                try:
                    if pair[0] not in guess or pair[0] in guess[pair[1]]:
                        match = False
                        break
                except: continue
            if match == True:
                filtered_guesses.append(guess)
        return filtered_guesses

    def filter_red(self, possible_guesses):
        filtered_guesses = []
        for guess in possible_guesses:
            match = True
            for letter in self._wrongLetters:
                if letter in guess:
                    match = False
                    break
            if match == True:
                filtered_guesses.append(guess)
        return filtered_guesses

    def filter_best(self, possible_guesses):
        filtered_words = []
        for letter in self._letters:
            filtered_words = [word for word in possible_guesses if letter in word]
            if not filtered_words:
                continue
            possible_guesses = filtered_words
        return possible_guesses

    def letter_counter(self, possible_guesses):
        word_counter = Counter()
        for word in possible_guesses:
            for i, letter in enumerate(word):
                if self._correctLetter[i] == "":
                    word_counter[letter] += 1
        sorted_letters = sorted(word_counter.items(), key=itemgetter(1), reverse=True)
        for letter in sorted_letters:
            self._letters.append(letter[0])