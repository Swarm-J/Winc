from helpers import random_koala_fact

__winc_id__ = "c0dc6e00dfac46aab88296601c32669f"
__human_name__ = "while"


def unique_koala_facts(number: int):
    facts = []
    fact_counter = 0
    while len(facts) != number:
        random_fact = random_koala_fact()

        if random_fact not in facts:
            facts.append(random_fact)
        elif fact_counter > 1000:
            break
        fact_counter += 1
    return facts


def num_joey_facts():
    unique_joey_facts = []
    particular_fact = random_koala_fact()
    fact_counter = 0

    while fact_counter < 11:
        random_fact = random_koala_fact()
        if particular_fact == random_fact:
            fact_counter += 1
        elif "joey" in random_fact:
            if random_fact not in unique_joey_facts:
                unique_joey_facts.append(random_fact)

    return len(unique_joey_facts)


def koala_weight():
    koala_weight = ''
    while True:
        random_fact = random_koala_fact()
        if "kg" in random_fact:
            weight_pos = random_fact.find('kg')
            koala_weight = random_fact[weight_pos-2:weight_pos]

            break
    
    return int(koala_weight)


# This block is only executed if this script is run directly (python main.py)
# It is not run if you import this file as a module.
if __name__ == "__main__":
    print(random_koala_fact())

    unique = unique_koala_facts(15)
    print(unique)
    
    joey = num_joey_facts()
    print(joey)

    weight = koala_weight()
    print(weight)
