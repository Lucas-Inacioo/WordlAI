import csv
import time
import dictionary
from player import Player
from wordle import Wordle

percentage = int(input("percentage of dict: "))
list = int(input("list: "))
word_list = dictionary.get_words(percentage, list)

def main():
    with open("wordlAI_data.csv", "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames = ["won/lose", "secret_word", "guess1", "guess2", "guess3", "guess4", "guess5", "guess6"])
        writer.writerow({"won/lose": 'won_lose', "secret_word": 'secret_word', "guess1": 'guess1', "guess2": 'guess2', "guess3": 'guess3', "guess4": 'guess4', "guess5": 'guess5', "guess6": 'guess6'})
    sample = int(input("sample: "))
    
    inicio = time.time()
    gamesWon = 0

    for _ in range(sample):
        wordle_match = Wordle(word_list)
        player = Player(word_list, wordle_match)
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
    print(f"Number of games won: {gamesWon}") 
    print(f"{sample} games played in %.2f seconds" % (fim-inicio))

if __name__ == "__main__":
    main()