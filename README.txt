WordlAI is an artificial intelligence capable of playing the browser game Wordle

Game 'Wordle' description:
    -A random 5-letter word is selected from a list.
    -Player has six attempts to try guessing the secret word.
    -After each attempt, the player receives feedback about the inputted word.
    -If the feedback contains  a green square, it means that the inputted letter is in the right position.
    -If the feedback contains  a yellow square, it means that the inputted letter is not in the right position.
    -If the feedback contains a red square, it means that the secret word does not have the inputted letter.

Code usage:
    The user is asked for a 'sample', a 'list', and a 'percentage', which consists of 
    the number of matches, which list of words to use and what percentage of the list will be used.
    After that, a CSV file will show the results, along with a summary of execution time and number of wins
    will be printed

Dictionary.py
    Here, the list selected will be fetched and returned. list 1 consists of the whole English dictionary,
    list 2 is for test purposes and any other value will use Wordle's original list of words.

Player.py
    The player class will try to minimize the number of possible words at each guess, counting the letters
    of all the words in the list and filtering it using the feedback provided by the Wordle class.

Wordle.py
    A basic implementation of the rules described above.

Project.py
    Requests the user for inputs used, instantiates both Player and Wordle, and exports results to a CSV file.