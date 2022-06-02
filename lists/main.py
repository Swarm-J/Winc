# Do not modify these lines
__winc_id__ = '6eb355e1a60f48a28a0bbbd0c88d9ab4'
__human_name__ = 'lists'

# Add your code after this line

def alphabetical_order(movies):
    list_of_movies = [movie for movie in sorted(movies)]
    
    return list_of_movies

def won_golden_globe(film: str):
    award_winning_movies = ["Jaws", "Star Wars: Episode IV - A New Hope", "E.T. the Extra-Terrestrial", "Memoirs of a Geisha"]
    for movie in award_winning_movies:
        if film.lower() == movie.lower():
            return True
    else:
        return False

def remove_toto_albums(albums):
    toto_albums = ["Fahrenheit", "The Seventh One" "Toto XX", "Falling in Between", "Toto XIV", "Old Is New"]
    for toto_album in toto_albums:
        if toto_album in albums:
            albums.remove(toto_album)
    return albums

test_albums = ["Black", "Old Is New", "Yes", "Fahrenheit"]

lol = remove_toto_albums(test_albums)
print(lol)