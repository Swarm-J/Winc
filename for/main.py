from helpers import get_countries


""" Leave this untouched. Wincpy uses it to match this assignment with the
tests it runs. """
__winc_id__ = "c545bc87620d4ced81cbddb8a90b4a51"
__human_name__ = "for"


""" Write your functions here. """
def shortest_names(countries):
    length_names = [len(country) for country in countries]
    shortest_country_name = min(length_names)
    countries = [country for country in countries if len(country) <= shortest_country_name]

    return countries
    
def most_vowels(countries):
    vowels = 'aeiou'
    amount_vowels = []
    country_vowels = []
    for country in countries:
        vowel_country_counter = 0
        for c in country.lower():
            if c in vowels:
                vowel_country_counter += 1
        country_vowels.append((vowel_country_counter, country))
        amount_vowels.append(vowel_country_counter)
    
    sort_amount_vowels = sorted(amount_vowels)
    top_three_amount_vowels = sort_amount_vowels[-3:]
    countries_highest_vowels = []
    for country_vowel in country_vowels:
        if country_vowel[0] >= top_three_amount_vowels[0]:
            countries_highest_vowels.append(country_vowel[1])
    
    return countries_highest_vowels[::-1]
    # return sorted(country_vowels)

def alphabet_set(countries):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    country_alphabet = ''
    country_names = []
    for country in countries:
        for c in country:
            if c in alphabet:
                if c in country_alphabet:
                    continue
                else: 
                    country_alphabet += c.lower()
                    if country in country_names:
                        continue
                    else:
                        country_names.append(country)
            else: 
                continue
    
    return country_names

# This block is only run if this file is the entrypoint; python main.py
# It is not run if it is imported as a module: `from main import *`
if __name__ == "__main__":
    countries = get_countries()

    """ Write the calls to your functions here. """
    short_names = shortest_names(countries)
    print(short_names)

    vowels = most_vowels(countries)
    print(vowels)

    alpha = alphabet_set(countries)
    print(alpha)
    