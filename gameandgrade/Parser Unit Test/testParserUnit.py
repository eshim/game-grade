'''
Created on June 5, 2013

@author: Eugene Shim

    This module is designed to test the gameandgrade 'parser' module outside of the web interface

    
    'CustomResult' class
    
    'GeneralParserTestSuite' class

        
'''
#Standard library modules
import shlex
import unittest
import subprocess
#module being tested
import gameAndGradeParser


#global variables for filenames
GOODCODEIN = 'good_code.py'
GOODCODEOUT = 'good_code_pylint.py'
BADCODEIN = 'bad_code.py'
BADCODEOUT = 'bad_code_pylint.py'
EMPTYCODEIN = 'empty_code.py'
EMPTYCODEOUT = 'empty_code_pylint.py'


#move this and refactor it to atch gameAndGradeParser
#maybe set up a parser class


class GeneralParserTestSuite(unittest.TestCase):
    """Class of unit tests for general issues"""
    
    def setUp(self):
        # run pylintEvaluate to create the pylint files
        gameAndGradeParser.pylintEvaluate(GOODCODEIN, GOODCODEOUT)
        gameAndGradeParser.pylintEvaluate(EMPTYCODEIN, EMPTYCODEOUT)
        gameAndGradeParser.pylintEvaluate(BADCODEIN, BADCODEOUT)

    def test_emptyOrGood(self):
        """This test checks if the parser module distinguishes between empty and good code"""
        self.assertNotEqual(gameAndGradeParser.readable_output(GOODCODEOUT), 
                         gameAndGradeParser.readable_output(EMPTYCODEOUT), 
                         "parser should distinguish between good and no code")
        
    def test_emptyOrBad(self):
        """This test checks if the parser module distinguishes between empty and bad code"""
        self.assertNotEqual(gameAndGradeParser.readable_output(BADCODEOUT), 
                         gameAndGradeParser.readable_output(EMPTYCODEOUT), 
                         "parser should distinguish between empty and bad code")
    
    def test_badOrGood(self):
        """This test checks if the parser module distinguishes between bad and good code"""
        self.assertNotEqual(gameAndGradeParser.readable_output(GOODCODEOUT), 
                         gameAndGradeParser.readable_output(BADCODEOUT), 
                         "parser should distinguish between bad and good code")
        
    def test_goodOutput(self):
        """This test checks if the parsed output for good code is an empty string"""
        self.assertNotEqual(gameAndGradeParser.readable_output(GOODCODEOUT), "", 
                         "parser should have some output")
        
    def test_badOutput(self):
        """This test checks if the parsed output for bad code is an empty string"""
        self.assertNotEqual(gameAndGradeParser.readable_output(BADCODEOUT), "", 
                         "parser should have some output")

    def test_emptyOutput(self):
        """This test checks if the parsed output for empty code is an empty string"""
        self.assertNotEqual(gameAndGradeParser.readable_output(EMPTYCODEOUT), "", 
                         "parser should have some output")
        

class PylintCodeTestSuite (unittest.TestCase):
    """Class of unit tests for specific pylint codes"""
    
    # Test for missing docstring (C0111)
    @unittest.skip("pylint codes for later")
    def test_pylintDocstring(self):
        """This test checks if the parser correctly determines that a docstring is absent"""
        self.assertRegexpMatches(gameAndGradeParser.readable_output(BADCODEOUT), 
                        r'%s Missing docstring' % (gameAndGradeParser.DIG), 
                         "parser should be able to locate a docstring")
        
    #Test that operator not preceded by space (C0322)
    @unittest.skip("pylint codes for later")
    def test_pylintSpacePrecedingOperator(self):
        """This test checks if the parser correctly determines that a docstring is absent"""
        self.assertRegexpMatches(gameAndGradeParser.readable_output(BADCODEOUT), 
                        r'%s Operator not preceded by a space' % (gameAndGradeParser.DIG), 
                         "parser should be able to identify the lack of a preceding space before an operator")


def parserTestSuite():
    """This is a function that aggregates all test cases into one test suite"""
    testList = (GeneralParserTestSuite, PylintCodeTestSuite) # needs to be updated for each new test suite
    
    suite = unittest.TestSuite()   # instantiate suite 
    
    for test_class in testList: #add all test cases from each test class to the suite
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
        
    return suite
    
if __name__ == '__main__':
    unittest.main(verbosity=2)




