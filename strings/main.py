# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

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

player = "Marco van Basten"

first_name = player[:player.find(" ")]
print(len(first_name))

last_name_len = len(player[player.find(" ") + 1:])
print(last_name_len)

name_short = f"{player[0]}.{player[player.find(' '):]}"
print(name_short)

full_chant = (f'{player[:player.find(" ")]}! ') * len(player[:player.find(" ")])
chant = full_chant[:-1]
print(chant)

good_chant = chant[-1] != ' '
print(good_chant)