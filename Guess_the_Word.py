from random import choice
from termcolor import colored
import pandas as pd


# set the colored tiles
tiles = {
    'correct__letter_correct_place': '🟩',
    'correct_letter_incorrect_place': '🟨',
    'incorrect': '🟥'
}


def validator(guess, answer):
    guessed = []
    tile_pattern = []

    # checking all letter in the guess
    for i, letter in enumerate(guess):
        # check if the letter in a correct place, colored it letter and place in green
        if answer[i] == guess[i]:
            guessed += colored(letter, 'green')
            tile_pattern.append(tiles['correct__letter_correct_place'])

            # replace letter in answer with '-'
            answer = answer.replace(letter, '-', 1)
        elif letter in answer:
            # if letter in answer, but in incorrect place
            guessed += colored(letter, 'yellow')
            tile_pattern.append(tiles['correct_letter_incorrect_place'])

            # replace letter in answer with '-'
            answer = answer.replace(letter, '-', 1)
        else:
            # if letter doesn't exist in answer
            guessed += colored(letter, 'red')
            tile_pattern.append(tiles['incorrect'])

    # def return joined colored letter and tile pattern
    return ''.join(guess), ''.join(tile_pattern)


tries = 6

# choosing language
language = str(input('Choose language to play (en/ru): ').lower())

if language == 'en':
    english_words_df = pd.read_csv('english_words.csv')
    # format df to list for quicker extraction word to random module
    english_words_list = list(english_words_df.astype(str).word.values)

    # all words to uppercase like in wordle
    words = [w.upper() for w in english_words_list]

    # select random word from list
    word = choice(words)
elif language == 'ru':
    russian_words_df = pd.read_csv('russian_words.txt')

    # format df to list for quicker extraction word to random module
    russian_words_list = list(russian_words_df.astype(str).word.values)

    # all words to uppercase like in wordle
    words = [wr.upper() for wr in russian_words_list]

    # select random word from list
    word = choice(words)


def game(target_word):
    end_game = False
    previous_guess = []
    tiles_pattern = []
    colored_guess = []

    # playing while player find correct answer or uses all attempts
    while not end_game:
        # input guess
        guess = input().upper()

        bad_guess = True

        # checking users guess
        while bad_guess:
            # checking if player use inputting guess
            if guess in previous_guess:
                print("You can't remember? You guessed this word! Try harder.")
                guess = input().upper()
            elif len(guess) != 5:
                print("The word must be with a 5 letter. Please, try again.")
                guess = input().upper()
            elif (guess not in words) or (guess not in words):
                print("That word doesn't exist. Please, try again")
                guess = input().upper()
            else:
                # if all correct
                bad_guess = False

        # append valid guess to previous list
        previous_guess.append(guess)

        # validate the guess
        guessed, pattern = validator(guess, target_word)

        # append result of validation
        colored_guess.append(guessed)
        tiles_pattern.append(pattern)

        # print the result of validation
        for gs, pn in zip(colored_guess, tiles_pattern):
            print(f'{gs}  {pn}')

        if guess == target_word or len(previous_guess) == tries:
            print(f'Well done! You needed {len(previous_guess)} tries to guess {target_word}')
            another_try = input('Do you want play one more time? y/n: ').lower()
            if another_try == 'y':
                game(word)
            else:
                print('Thank You for playing this game. Bye!')
            end_game = True

        # print the result of the game
        if (len(previous_guess) == tries) and (guess != target_word):
            print(f'GAME OVER! You out of the tries. The correct word was {target_word}')

            another_try = input('Do you want play one more time? y/n: ').lower()
            if another_try == 'y':
                game(word)
            else:
                print('Thank You for playing this game. Bye!')


print(colored('Welcome to the word guess game by A. L.', 'green'))
print()
print(f'You have {tries} to guess the word. Let\'s go!')
game(word)
