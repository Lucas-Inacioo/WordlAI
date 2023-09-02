from collections import Counter
from operator import itemgetter
import random
import csv
import time
import dictionary 

percentage = int(input("percentage of dict: "))
word_list = dictionary.get_words(percentage)
class Wordle():
    def __init__(self):
        self.tries = 0
        self.secret_word = random.choice(word_list)
        self.case = 0
    
    def matches(self, guessed_word):
        self.tries += 1
        feedback = []
        for i in range(5):
            guessedLetter = guessed_word[i]
            if guessedLetter == self.secret_word[i]:
                feedback.append("🟩")
            elif guessedLetter in self.secret_word:
                feedback.append("🟨")
            else:
                feedback.append("🟥")
        stringFeedback = ""
        for letter in feedback:
            stringFeedback += letter
        print(stringFeedback)
        self.feedback = feedback

    def verify_end_game(self):
        if self.feedback == ['🟩', '🟩', '🟩', '🟩', '🟩']:
            return True
        else:
            return False

def main():
    inicio = time.time()
    with open("wordlAI_data.csv", "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames = ["won/lose", "secret_word", "guess1", "guess2", "guess3", "guess4", "guess5", "guess6"])
        writer.writerow({"won/lose": 'won_lose', "secret_word": 'secret_word', "guess1": 'guess1', "guess2": 'guess2', "guess3": 'guess3', "guess4": 'guess4', "guess5": 'guess5', "guess6": 'guess6'})

    sample = int(input("sample: "))
    gamesWon = 0

    for _ in range(sample):
        global letters, wrongLetters, knownLettersPositions
        letters = []
        wrongLetters = set()
        knownLettersPositions = set()
        allInputs = []
        inputWord = random.choice(filter_best(word_list))
        allInputs.append(inputWord)
        print(inputWord)
        wordle_match = Wordle()
        wordle_match.matches(inputWord)
        result = 0
        if wordle_match.verify_end_game():
            result = 1
            gamesWon = gamesWon + 1
            continue
        else:
            while wordle_match.tries < 6:
                inputWord = ai(word_list, wordle_match, allInputs)    
                allInputs.append(inputWord)
                print(inputWord)
                wordle_match.matches(inputWord)
                if wordle_match.verify_end_game():
                    result = 1                
                    gamesWon = gamesWon + 1
                    break
        with open("wordlAI_data.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["won/lose", "secret_word", "guess0", "guess1", "guess2", "guess3", "guess4", "guess5"])
            all_inputs = [allInputs[i] if i < len(allInputs) else None for i in range(6)]
            
            writer.writerow({
                "won/lose": result,
                "secret_word": wordle_match.secret_word,
                "guess0": all_inputs[0],
                "guess1": all_inputs[1],
                "guess2": all_inputs[2],
                "guess3": all_inputs[3],
                "guess4": all_inputs[4],
                "guess5": all_inputs[5]
            })
    fim = time.time()
    print(f"Number of games won: {gamesWon}") 
    print(f"{sample} games played in %.2f seconds" % (fim-inicio))

def ai(possible_guesses, wordle_match, allInputs):
        possible_guesses = filter_green(possible_guesses, wordle_match, allInputs)
        possible_guesses = filter_yellow(possible_guesses, wordle_match, allInputs)
        possible_guesses = filter_red(possible_guesses, wordle_match, allInputs)
        possible_guesses = filter_best(possible_guesses)
        best_guess = random.choice(possible_guesses)     
        return best_guess

def filter_green(possible_guesses, wordle_match, allInputs):
    lastInput = allInputs[-1]
    correctLetter = ["", "", "", "", ""]
    filtered_guesses = []
    for i in range(5):
        if wordle_match.feedback[i] == "🟩":
            correctLetter[i] = lastInput[i]
    for guess in possible_guesses:
        match = True
        for i in range(5):
            if correctLetter[i] != "" and correctLetter[i] != guess[i]:
                match = False
                break
        if match == True:
            filtered_guesses.append(guess)

    return filtered_guesses

def filter_yellow(possible_guesses, wordle_match, allInputs):
    lastInput = allInputs[-1]
    filtered_guesses = []
    for i in range(5):
        if wordle_match.feedback[i] == "🟨":
            knownLettersPositions.add((lastInput[i], i))
    for guess in possible_guesses:
        match = True
        for pair in knownLettersPositions:
            if pair[0] not in guess or pair[0] in guess[pair[1]]:
                match = False
                break
        if match == True:
            filtered_guesses.append(guess)
    return filtered_guesses

def filter_red(possible_guesses, wordle_match, allInputs):
    lastInput = allInputs[-1]
    filtered_guesses = []
    for i in range(5):
        if wordle_match.feedback[i] == "🟥":
            if lastInput[i] in letters:
                letters.remove(lastInput[i])
            wrongLetters.add(lastInput[i])
    for guess in possible_guesses:
        match = True
        for letter in wrongLetters:
            if letter in guess:
                match = False
                break
        if match == True:
            filtered_guesses.append(guess)
    return filtered_guesses

def filter_best(possible_guesses):
    filtered_words = []
    letter_counter(possible_guesses)
    for letter in letters:
        filtered_words = [word for word in possible_guesses if letter in word]
        if not filtered_words:
            continue
        possible_guesses = filtered_words
    return possible_guesses

def letter_counter(possible_guesses):
    word_counter = Counter()
    for result in possible_guesses:
        word = result.lower().rstrip()
        for letter in set(word):
            word_counter[letter] += 1
    sorted_letters = sorted(word_counter.items(), key=itemgetter(1), reverse=True)
    for letter in sorted_letters:
        letters.append(letter[0])

if __name__ == "__main__":
    main()