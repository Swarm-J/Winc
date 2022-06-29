__winc_id__ = "9920545368b24a06babf1b57cee44171"
__human_name__ = "refactoring"

alice_name = "Alice Aliceville"
alice_profession = "electrician"
bob_name = "Bob Bobsville"
bob_profession = "painter"
craig_name = "Craig Craigsville"
craig_profession = "plumber"

alfred_name = "Alfred Alfredson"
alfred_address = "Alfredslane 123"
alfred_needs = ["painter", "plumber"]
bert_name = "Bert Bertson"
bert_address = "Bertslane 231"
bert_needs = ["plumber"]
candice_name = "Candice Candicedottir"
candice_address = "Candicelane 312"
candice_needs = ["electrician", "painter"]

alfred_contracts = []
for need in alfred_needs:
    if need == alice_profession:
        alfred_contracts.append(alice_name)
    elif need == bob_profession:
        alfred_contracts.append(bob_name)
    elif need == craig_profession:
        alfred_contracts.append(craig_name)

bert_contracts = []
for need in bert_needs:
    if need == alice_profession:
        bert_contracts.append(alice_name)
    elif need == bob_profession:
        bert_contracts.append(bob_name)
    elif need == craig_profession:
        bert_contracts.append(craig_name)

candice_contracts = []
for need in candice_needs:
    if need == alice_profession:
        candice_contracts.append(alice_name)
    elif need == bob_profession:
        candice_contracts.append(bob_name)
    elif need == craig_profession:
        candice_contracts.append(craig_name)

print("Alfred's contracts:", alfred_contracts)
print("Bert's contracts:", bert_contracts)
print("Candice's contracts:", candice_contracts)

class Homeowner():

    def __init__(self, name: str, address: str, needs: list):

        self.name = name
        self.address = address
        self.needs = needs

    def contracts(self):
        contractor_names = getattr(Specialist, 'prof_list')
        contractors = []
        cheapest_contractors = []
        
        for need in self.needs:
            for c in contractor_names:
                if need == c['profession']:

                    contractors.append(c)
            
            contractors.sort(key=lambda contractors: contractors['price'])
            cheapest_contractors.append(contractors[0]['name'])
            contractors = []            
                   
        return f"{self.name}'s contracts: {cheapest_contractors}"


class Specialist():
    
    prof_list = []

    def __init__(self, name: str, profession:str, price: float):

        self.name = name
        self.profession = profession
        self.prof_list.append({"name": name, "profession": profession, "price": price})
        self.price = price


class Electrician(Specialist):

    def __init__(self, name: str, profession: str, price: float):
        super().__init__(name, profession, price)

        self.profession = "electrician"


class Painter(Specialist):

    def __init__(self, name: str, profession: str, price: float):
        super().__init__(name, profession, price)

        self.profession = "painter"

class Plumber(Specialist):

    def __init__(self, name: str, profession: str,  price: float):
        super().__init__(name, profession, price)

        self.profession = "plumber"


if __name__ == "__main__":

    alfred_alfredson = Homeowner("Alfred Alfredson", "Alfredslane 123", ["painter", "plumber"])
    bert_bertson = Homeowner("Bert Bertson", "Bertslane 231", ["plumber"])
    candice_candicedottir = Homeowner("Candice Candicedottir", "Candicelane 312", ["electrician", "painter"])
    
    alice_aliceville = Electrician("Alice Aliceville","electrician", 1500)
    peter_parker = Electrician("Peter Parker", "electrician", 1100)
    bob_bobsville = Painter("Bob Bobsville", "painter", 1500)
    craig_craigsville = Plumber("Craig Craigsville", "plumber", 1200)
    bruce_banner = Plumber("Bruce Banner", "plumber", 1250)

    # print(candice_candicedottir.address)
    # print(craig_craigsville.price)
    # print(bob_bobsville.profession)
    # print(Specialist.prof_list)

    test = alfred_alfredson.contracts()
    print(test)
    test2 = bert_bertson.contracts()
    print(test2)
    test3 = candice_candicedottir.contracts()
    print(test3)
    
    print(bruce_banner.profession)