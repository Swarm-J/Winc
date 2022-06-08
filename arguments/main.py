# Do not modify these lines
__winc_id__ = '7b9401ad7f544be2a23321292dd61cb6'
__human_name__ = 'arguments'


# Add your code after this line
def greet(name, greeting='Hello, <name>!'):
    greeting = greeting.replace('<name>', name)

    return greeting


def force(mass, body='earth'):

    surface_gravity = {
                        "sun": 274,
                        "jupiter": 24.9,
                        "neptune": 11.2,
                        "saturn": 10.4,
                        "earth": 9.8,
                        "uranus": 8.9,
                        "venus": 8.9,
                        "mars": 3.7,
                        "mercury": 3.7,
                        "moon": 1.6,
                        "pluto": 0.6
                        }

    return round((mass * surface_gravity[body]), 1)


def pull(m1, m2, d):
    g = 6.674*(10**-11)
    f = g * ((m1 * m2) / (d ** 2))

    return f


check = greet('Bob', "What's up, <name>!")
print(check)
c = greet('Bob')
print(c)

test = force(50)
print(test)
test_again = force(50, 'mars')
print(test_again)

example1 = pull(800, 1500, 3)
print(example1)

example2 = pull(0.1, 5.972*1024**24, 6.371*10**6)
print(example2)
