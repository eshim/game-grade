'''
Created on July 22, 2013

@author: Eugene Shim

    This unittest suite is an example of a unittest file to be passed into GameandGrade through 
    the admin interface to be automatically run when students upload files. No test fixture has
    to be provided. Given that the filename follows the correct convention by begining with the
    word "test", it will be detected and be run on the specified module.

    Further reading/examples are provided by Python can be found in the following link as of July
    22, 2013. http://docs.python.org/2/library/unittest.html
        
'''

# This is the module chosen to be tested. When creating each task, instructors must specify a 
# filename that their students' uploads will copy to help ensure that unittests are run 
# correctly.
import fizzbuzz_correct

import unittest # This is a required import for unittesting
import sys, inspect #This is a required import for isfunction() and getmodule()

class fizzbuzzTestSuite(unittest.TestCase):
    """A suite of unittest cases"""
    
    def is_mod_function(mod, func):
        """ 
        Helper function that tests that the function 'func' is a function and that the 
        functions are from that module "mod"
        """
        
        return inspect.isfunction(func) and inspect.getmodule(func) == mod
    
    knownIfFizzBuzz = ( (3, "Fizz!"),
                    (5, "Buzz!"),
                    (10, "Buzz!"),
                    (15, "FizzBuzz!") ) 
    
    
    def test_search_function(self):
        """
        Searches the module named "prime" for the function named "IsPrime".
        The term 'test' is NECESSARY for detection as a unittest case.
        Notice that this docstring also serves as the message/label for the
        unit test check on the web-application.
        """
        
        isThereCheck = False
        
        for function in fizzbuzz_correct.__dict__.itervalues():  
            # Check each function in the module fizzbuzz for one named "fizzbuzz"
            if is_mod_function(fizzbuzz_correct, function) and function.__name__ == "fuzzbuzz":
                isThereCheck = True
                
        self.assertEquals(isThereCheck, True, "The function isn't correctly defined.")
        # If isThereCheck is not equal to True, then print the message
    
    
    def test_function_output(self):
        """
        Thisfunction should return correct output. This test spot-checks 
        fizzbuzz() for the the values given in knownIfPrime.
        """
        
        for integer, stringValue in self.knownIfPrime: # Check each tuple in knownIfPrime
            result = fizzbuzz_correct.fizzbuzz(integer)
            
            self.assertEquals(stringValue, result, "This doesn't seem to work with %d" % (integer))
            
            
    def test_function_edge_case(self):
        """
        This function checks whether fizzbuzz() will return the correct
        value for a specific value.
        """
        
        result = fizzbuzz_correct.fizzbuzz(15)
        
        self.assertEquals("FizzBuzz!", result, "This doesn't seem to work with %d" % (integer))
        
        
        
        
        
    