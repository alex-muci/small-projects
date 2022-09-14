import json
from difflib import get_close_matches

def read_json(file_name):
    with open(file_name, 'rb') as file:
        return json.load(file)

def word_finder(w: str, dictionary_data: str) -> str:
    dictionary = read_json(dictionary_data)
    w.lower()

    if w in dictionary: res = dictionary[w]
    elif w.title() in dictionary:  # if "texas" entered also "Texas" will be checked
        res = dictionary[w.title()]
    elif w.upper() in dictionary:  # e.g. USA, NATO, ...
        res = dictionary[w.upper()]
    else: # try and get the closest word, and ask user
        close_word = get_close_matches(w, dictionary)
        if close_word:  # not empty
            yn = input(f"Did you mean '{close_word[0]}'? Y for yes and N for no: ")
            if yn == "Y": res = dictionary[close_word[0]]
            elif yn == "N": res = "Cannot find such word."
            else: res = "No such an option. Goodbye."
        else:
            res = "Cannot find such word or similar words to suggest."

    # check that it is not an error (not a list of meanings)
    if not isinstance(res, list): return "\n" + res +"\n"

    # loop through list of meanings (or removing [] if one)
    result = "\n"
    for m in res:
        result +=  m + "\n"
    return result


if __name__ == "__main__":

    word = input("Find following word in the dictionary: ")
    print(word_finder(word, "dictionary_data.json"))
