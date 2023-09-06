#https://gist.github.com/iancward/afe148f28c5767d5ced7a275c12816a3

import re
import requests
import random
def get_words(percentage, list):
    if (list == 1):
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage should be between 0 and 100")
        
        meaningpedia_resp = requests.get("https://meaningpedia.com/5-letter-words?show=all")
        pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
        words = pattern.findall(meaningpedia_resp.text)
        words.remove('FALSE')
        
        num_words_to_return = int(len(words) * (percentage / 100))
        random.shuffle(words) 
        selected_words = words[:num_words_to_return]
    elif (list == 2):
        selected_words = ["aesir", "rosed", "carga", "rotte", "wxyzh"]
    else:
        urlGuesses = "https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw"
        urlAnswers = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/1792f853e1cd0249f7588c724e00d46dbc4894eb/wordle-answers-alphabetical.txt"

        response = requests.get(urlGuesses)
        guesses = response.text.splitlines()

        response = requests.get(urlAnswers)
        answers = response.text.splitlines()
        return guesses, answers

    return selected_words
