# Do not modify these lines
__winc_id__ = '04da020dedb24d42adf41382a231b1ed'
__human_name__ = 'classes'

# Add your code after this line

class Player():

    def __init__(self, name, speed, endurance, accuracy):

        self.name = name
        self.speed = speed
        self.endurance = endurance
        self.accuracy = accuracy

        if not 0 <= speed <= 1 or not 0 <= endurance <= 1 or not 0 <= accuracy <= 1:
            raise ValueError("Number must be between 0 and 1")

    def introduce(self):
        return f"Hello everyone, my name is {self.name}."


    def strength(self):
        player_stats = [[self.speed, 'speed'], [self.endurance, 'endurance'], [self.accuracy, 'accuracy']]
        highest_stat = max(player_stats)

        return (highest_stat[1], highest_stat[0])

class Commentator():

    def __init__(self, name):

        self.name = name

    def sum_player(self, player):
        speed = getattr(player, 'speed')
        endurance = getattr(player, 'endurance')
        accuracy = getattr(player, 'accuracy')
        
        attributes = speed + endurance + accuracy

        return attributes

    def compare_players(self, player_one, player_two, attribute):
        attscore_player_one = getattr(player_one, attribute) 
        attscore_player_two = getattr(player_two, attribute)

        if attscore_player_one == attscore_player_two:
            if getattr(player_one, 'strength')() == getattr(player_two, 'strength')():
                if getattr(self, 'sum_player')(player_one) > getattr(self, 'sum_player')(player_two):
                    return getattr(player_one, 'name')
                elif getattr(self, 'sum_player')(player_one) < getattr(self, 'sum_player')(player_two):
                    return getattr(player_two, 'name')
                else: 
                    return 'These two players might as well be twins!'
            elif getattr(player_one, 'strength')() > getattr(player_two, 'strength')():
                return getattr(player_one, 'name')
            else:
                return getattr(player_two, 'name')
        elif attscore_player_one > attscore_player_two:
            return getattr(player_one, 'name')
        else:
            return getattr(player_two, 'name')



def main():
    p1 = Player('Julian', 1, 1, 1)
    # print(p1.speed)
    # print(p1.endurance)
    # print(p1.accuracy)

    print(p1.introduce())

    print(p1.strength())

    ray = Commentator('Ray Hudson')
    print(ray.name)

    print(ray.sum_player(p1))

    p2 = Player('Guus', 1, 1, 0)
    print(ray.compare_players(p1, p2, 'endurance'))

    # t = getattr(p2, 'strength')()
    # print(t)

    # t2 = getattr(ray, 'sum_player')(p2)
    # print(t2)

if __name__ == "__main__":
    main()