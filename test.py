import os
# player_stats = [(0.5, 'speed'), (1, 'endurance'), (0, 'accuracy')]
# highest_stat = sorted(player_stats)[-1]
# print(highest_stat)
# print(sorted(player_stats))
directory = 'cache'
cd = os.getcwd() + '/files'
combi = os.path.join(cd, directory)
print(combi)
print(cd)