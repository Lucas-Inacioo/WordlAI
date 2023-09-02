#https://gist.github.com/iancward/afe148f28c5767d5ced7a275c12816a3
import re
import requests
import random

def get_words(percentage):
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage should be between 0 and 100")
    
    meaningpedia_resp = requests.get("https://meaningpedia.com/5-letter-words?show=all")
    pattern = re.compile(r'<span itemprop="name">(\w+)</span>')
    words = pattern.findall(meaningpedia_resp.text)
    
    num_words_to_return = int(len(words) * (percentage / 100))
    random.shuffle(words) 
    selected_words = words[:num_words_to_return]
    
    return selected_words

