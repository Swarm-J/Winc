# Do not modify these lines
__winc_id__ = '63ce21059cf34d3d8ffef497ede7e317'
__human_name__ = 'comments'

# Add your code after this line

"""The next block of code is used to illustrate my understanding of comments. The functions are simplistic
examples to demonstrate the possible use of comments.
"""

# Function to calculte the multiplication of x and y
def multiply(x, y):
    """Returns the result of multiplying x and y. Variables can be either
    ints or string and int."""
    return x * y

test = multiply('a', 5)     # Create a variable to test the function
print(test)     # prints the result of 'test'

def greetings(name):
    """Simple function to greet the user. Function takes both
    strings and integers."""
    return f"Greetings from earth, {name}!"

print(greetings('Julian'))