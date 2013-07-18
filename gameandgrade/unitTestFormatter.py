'''
Created on June 10 2013

@author: Eugene Shim

    This module is merely a unit test that loads all of the test
    cases based on the directory passed in the command line. It
    then outputs the stderr to a logfile in the given directory.
    
    Used by issuing: $ python unitTestFormatter.py <pathToDirectoryOfUnitTests>
        
'''
#Standard library modules
import unittest
import os
import sys

unitTestDirectory = str(sys.argv[1]) # The directory where unit test cases are to be loaded ('Parser\ Unit\ Test')

def main():
    """Main method to run the unit test"""   
    suite = unittest.TestLoader().discover(unitTestDirectory) 
    os.chdir(os.path.join(os.getcwd(), unitTestDirectory)) #need to change cwd if the unit test runs files that it doesn't just import
    
    f = open('log_file.txt', 'w')
    testRunner = unittest.TextTestRunner(f, verbosity=2).run(suite) #diverts stderr to the log_file when running the test suite
    f.close()
    
    
if __name__ == '__main__':
    main()