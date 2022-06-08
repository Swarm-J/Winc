# Do not modify these lines
from helpers import get_countries

__winc_id__ = "00a4ab32f1024f5da525307a1959958e"
__human_name__ = "dictionariesv2"

# Add your code after this line
def create_passport(name, date_of_birth, place_of_birth, height, nationality):
    passport = {
                'name': name,
                'date_of_birth': date_of_birth,
                'place_of_birth': place_of_birth,
                'height': height,
                'nationality': nationality,
            }

    return passport


def add_stamp(passport, country):

    if passport['nationality'] is not country:

        if 'stamps' not in passport.keys():
            passport['stamps'] = [country]
        else:
            if country not in passport.items():
                passport['stamps'].append(country)
        
    return passport


def add_biometric_data(passport, type, value, date):

    if 'biometric' in passport.keys():

        if type not in passport['biometric'].keys():

            update_biometric = {
                                type: {
                                'value': value,
                                'date': date
                                }}
            passport['biometric'].update(update_biometric)
        else:
            passport['biometric'][type]['value'] = value
            passport['biometric'][type]['date'] = date
        
    else:
        passport['biometric'] = {
                                type: { 
                                'value': value,
                                'date': date
                                }}

    return passport

js = create_passport('Julian Schinkel', '1987-01-1987', 'Zwolle', 1.86, 'Netherlands')
print(js)

d = {'name': 'Julian Schinkel', 'date_of_birth': '1987-01-1987', 'place_of_birth': 'Zwolle', 'height': 1.86, 'nationality': 'Netherlands', 'stamps': ['Belgium'], 'biometric': {'eye_color_left': {'value': 'blue', 'date': '2022-06-06'}}}
print(d)

kekw = add_stamp(d, 'Germany')
print(kekw)

test = {'name': 'Julian Schinkel', 'date_of_birth': '1987-01-1987', 'place_of_birth': 'Zwolle', 'height': '1.86', 'nationality': 'Netherlands', 'biometric': {'eye_color_left': {'value': 'blue', 'date': '2022-06-06'}}}
bio = add_biometric_data(test,"eye_color_right", "red", "2022-06-07")
print(bio)
