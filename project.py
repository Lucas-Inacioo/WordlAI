import csv
import time
import dictionary
from player import Player
from wordle import Wordle

print("\nWelcome to WordlAI, please, choose a list: \n")

print("\nList 1: English Dictionary")
print("List 2: BugFix")
print("List 3: Wordle's Official List\n")
list = int(input("list: "))

if (list == 1 or list == 2):
    percentage = int(input("Percentage of dict: "))
    guessesList = dictionary.get_words(percentage, list)
    answersList = guessesList
else:
    result = dictionary.get_words(0, list)
    guessesList = result[0]  
    answersList = result[1]

def main():
    with open("wordlAI_data.csv", "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames = ["won/lose", "secret_word", "guess1", "guess2", "guess3", "guess4", "guess5", "guess6"])
        writer.writerow({"won/lose": 'won_lose', "secret_word": 'secret_word', "guess1": 'guess1', "guess2": 'guess2', "guess3": 'guess3', "guess4": 'guess4', "guess5": 'guess5', "guess6": 'guess6'})
    
    sample = int(input("Sample: "))
    inicio = time.time()
    gamesWon = 0

    for _ in range(sample):
        wordle_match = Wordle(answersList)
        player = Player(guessesList, wordle_match)
        player.play()
        allInputs = player.getAllInputs()
        result = player.getResult()

        if (result): gamesWon += 1

        with open("wordlAI_data.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["won/lose", "secret_word", "guess0", "guess1", "guess2", "guess3", "guess4", "guess5"])
            all_inputs = [allInputs[i] if i < len(allInputs) else None for i in range(6)]
            
            writer.writerow({
                "won/lose": result,
                "secret_word": wordle_match.getSecretWord(),
                "guess0": all_inputs[0],
                "guess1": all_inputs[1],
                "guess2": all_inputs[2],
                "guess3": all_inputs[3],
                "guess4": all_inputs[4],
                "guess5": all_inputs[5]
            })
    fim = time.time()
    print(f"\nNumber of games won: {gamesWon}") 
    print(f"{sample} games played in %.2f seconds" % (fim-inicio))

if __name__ == "__main__":
    main()