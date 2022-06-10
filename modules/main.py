import this
from time import sleep
from math import sin
from datetime import datetime
import sys
from greet import supergreeting

# Do not modify these lines
__winc_id__ = '78029e0e504a49e5b16482a7a23af58c'
__human_name__ = 'modules'


# Add your code after this line
def wait(seconds):
    sleep(seconds)


def my_sin(number):
    return sin(number)


def iso_now():
    return datetime.now().strftime('%Y-%m-%dT%H:%M')      


def platform():
    return sys.platform


def supergreeting_wrapper(name):
    sgw = supergreeting(name)
    return sgw


# f1 = wait(5)
f2 = my_sin(10.5)
print(f2)
f3 = iso_now()
print(f3)
f4 = platform()
print(f4)
f5 = supergreeting_wrapper("Julian")
print(f5)