#https://gist.github.com/iancward/afe148f28c5767d5ced7a275c12816a3

import re
import requests
import random
def get_words(percentage, list):
    if (list == 1):
        if not 0 < percentage <= 100:
            raise ValueError("Percentage should be between 0 and 100")
        
        with requests.get("https://meaningpedia.com/5-letter-words?show=all") as response:
            pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
            words = pattern.findall(response.text)

        words.remove('FALSE')
        num_words_to_return = int(len(words) * (percentage / 100))
        random.shuffle(words) 
        selected_words = words[:num_words_to_return]
    elif (list == 2):
        selected_words = ["aesir", "rosed", "carga", "rotte", "wxyzh"]
    else:
        with open("answers.txt","r") as file:
            data = file.readlines()
            answers = []
            for item in data:
                answers.append(item.replace("\n",""))

        with open("guesses.txt","r") as file:
            data = file.readlines()
            guesses = []
            for item in data:
                guesses.append(item.replace("\n",""))

        return (answers + guesses), answers

    return selected_words
