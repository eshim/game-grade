"""
This file is to be used to test what 'perfect code' looks like in PyLint
"""
def fizzbuzz(count):
#    for count in range(1, 31):
    if count % 3 == 0 and count % 5 == 0: 
#        print "FizzBuzz!"
        return "FizzBuzz!"
    elif count % 3 == 0: 
#        print "Fizz!"
        return "Fizz!"
    elif count % 5 == 0: 
#        print "Buzz!"
        return "Buzz!"