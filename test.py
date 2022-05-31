# Add your code after this line
# Players that scored
scorer_1 = "Ruud Gullit"
scorer_2 = "Marco van Basten"

# Goals Scored during the match in minutes
goal_0 = 32
goal_1 = 54

scorers = scorer_1 + ' ' + str(goal_0) + ', ' + scorer_2 + ' ' + str(goal_1)
print(scorers)

report = f"{scorer_1} scored in the {goal_0}nd minute\n{scorer_2} scored in the {goal_1}th minute"
print(report)

player = "Frank Rijkaard"

first_name = player[player.find("Frank"):5]
print(first_name)

last_name_len = len(player[player.find("Rijkaard"):])
print(last_name_len)

name_short = f"{player[0]}. {player[player.find('Rijkaard'):]}"
print(name_short)

full_chant = (f'{player[player.find("Frank"):5]}! ') * len(player[player.find("Frank"):5])
chant = full_chant[:-1]
print(chant)

good_chant = chant[len(chant) - 1] != ' '
print(good_chant)
