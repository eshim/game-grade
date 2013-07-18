'''
Created on June 10 2013

@author: Eugene Shim

    This module is set up to take unit test log files and convert
    them into strings to have them be parsed into a list of tuples
    to be viewed on HTML
    
    convertFileToString() a helper function that converts text files to strings
    
    parseUnitTestResults() a function that parses text files for every text case result
        
    parseUnitTestSummary() a function that parses text files for the unit test summary
    
'''
#Standard library modules
import re


# regex string parsers for the unit test logs 
testStringSuccess = re.compile(r"""(?P<testName>\w+)\s       # testName (\w+ = a 1+ number of alphanumeric and underscore characters)
                                \((?P<testModule>\w+)[.]     # Opening parentheses, testModule, and one period
                                (?P<testClass>\w+)\)\n       # testClass, closing parentheses and a newline
                                (?P<testDocstring>.*)        # testDocString (.* any number of non-newline characters)
                                \s\.{3}\s                    # a space, three periods and one more space
                                (?P<testSuccess>.+)          # testSuccess
                                """,re.VERBOSE)

testSummaryReport = re.compile(r"""Ran\s                     # 'Ran '
                                (?P<testTotalNumber>\d+)     # testTotalNumber
                                .+\n\n                       # some uninteresting text with two newlines
                                (?P<totalTestResult>.+?)     # totalTestResult
                                (?:\s\(skipped=)?            # non-capturing and optional ' (skipped='
                                (?P<skippedTest>\d+?)?\)?$   # optional skippedTest and ')'
                                """,re.VERBOSE)


def convertFileToString(fileName):
    """Helper function that would read text files into a string"""
    
    with open(fileName) as log_file:
        logString = log_file.read()
        log_file.close()
        
        return logString
    
 
def parseUnitTestResults(unitTestLog):
    """A string parser that returns a list of the following tuple('testName', 'testModule', 'testClass', 'testDocstring','testSuccess')
    for each test case"""
    
    matchString = convertFileToString(unitTestLog)        
    testResults = re.findall(testStringSuccess, matchString)
    
    return testResults


#do I want to merge these two functions together and return one list of tuples to parse?
def parseUnitTestSummary(unitTestLog):
    """A string parser that returns a list of the following tuple ('testTotalNumber', 'totalTestResult', 'skippedTest') for the test
    summary report"""
    
    matchString = convertFileToString(unitTestLog)         
    testSummary = re.findall(testSummaryReport, matchString)
    
    return testSummary          



#def getter():
#def setter():