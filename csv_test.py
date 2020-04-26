import unittest 
from csv_project import main
import random
import string
letters = string.ascii_letters
keywords_test=["Waikato Region","Marlborough Region","Wellington Region"]
class SimpleTest(unittest.TestCase): 
  
    
     
    def test_file(self): 

        
        folder="phys-"+str(random.randrange(1,100000))
        # print(folder)

        rows_count=main(folder,random.choice(keywords_test))  
        # print(k)
        self.assertGreater(rows_count,0)

    

        
  
if __name__ == '__main__': 
    unittest.main() 