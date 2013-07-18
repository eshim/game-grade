'''
Created on Jul 18, 2012

@author: peter

Test suite designed to conduct sanity checks on TopSpector/config
file. Checks that things exist, point to the correct executables &etc.

If main method, only tests in this test suite are invoked.
'''
#Standard library modules
import os
import unittest
import ConfigParser
import subprocess


class ConfigTestSuite(unittest.TestCase):
    '''
    ConfigTestSuite subclasses unittest.TestCase.
    
    setUp method is run before every test.
    tearDown is run after. 
    
    Test cases:
    - test_configExists
        Makes sure the config file exists
    - test_configCanRead
        Makes sure the ConfigParser is capable of interpreting the file.
        Does NOT check to make sure all necessary items are included yet.
    - test_confSectionsExist
        Makes sure that the hadoop, weka and topspector sections are included 
        in the file. These sections configure HadoopControl, TopSpector and WekaInterface
        classes.
    - test_hadoopPrefixExists
        Checks the existence of the hadoop PREFIX setting (used to set HADOOP_PREFIX in
        any shells).
    - test_hadoopCmdExists
        Checks for the existence/availability of the hadoop command by appending bin to 
        the HADOOP_PREFIX
    - test_jythonJarExists
        Make sure the jython jar file exists
    - test_wekaJarExists
        Make sure the weka jar file exists
    
    The only file required to run these tests is: TopSpector/config
    
    Intended invocation of this file:
    java -Xmx1024M -jar jython.jar test_configParser
    
    or as part of the entire test suite. For more details see:
    
    '''
    def setUp(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('config')      
        
    def tearDown(self):
        del(self.config)  
    
    def test_configExists(self):
        self.assertTrue(os.path.exists('config'))
        
    def test_configCanRead(self):
        self.assertTrue(type(self.config.get('topspector','LOGS'))==str)
    
    def test_confSectionsExist(self):
        sections = self.config.sections()
        self.assertTrue('weka' in sections and 'hadoop' in sections and 'topspector' in sections)
    
    def test_hadoopPrefixExists(self):
        self.assertTrue(os.path.exists(self.config.get('hadoop','PREFIX')))
        
    def test_hadoopCmdExists(self):
        try:
            p = subprocess.Popen(os.path.join(self.config.get('hadoop','PATH'),'hadoop'),stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        except:
            self.assertTrue(False)
        else:
            self.assertTrue(True)
    
    def test_jythonJarExists(self):
        self.assertTrue(os.path.exists(self.config.get('topspector','JYTHON')))
        
    def test_wekaJarExists(self):
        self.assertTrue(os.path.exists(self.config.get('weka','JAR')))
            
def main():
    unittest.main()
    
if __name__=="__main__":
    main()