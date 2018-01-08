'''
Created on 06.01.2018

@author: Adrian Raul Mos
'''
import sys
sys.path.append('../')


import unittest
from descriptionprocessor import DescriptionProcessor




class TestDescriptionProcessor(unittest.TestCase):

    def test_MoveDashedLinesOnSeparateLine_InputRequiresNoMovement_NoMovementExpected(self):
        description = "a-ti a-si, ce-i, i-am, intr-un intr-o, l-am, sa-si sa-l si-a" \
                      " ultra-compact, mini-geam, anti-rasturnare, crescandu-l, dintr-o dintr-un," \
                      " non-toxic ultra-compact full-option nou-nascuti non-alergic," \
                      " non-toxice, nou-nascut, anti-alergic, anti-alergica"
        
        result = DescriptionProcessor._MoveDashedLinesOnNewRow(description)
        expected = description
        self.assertEqual(expected, result)

    def test2_MoveDashedLinesOnSeparateLine_NumberRanges_NoMovementExpected(self):
        description = "0-12 luni, 0-5ani 11-12 ani" 
        
        result = DescriptionProcessor._MoveDashedLinesOnNewRow(description)
        expected = description
        self.assertEqual(expected, result)

    def test_MoveDashedLinesOnSeparateLine_BreakRequired_BreakIsIncluded(self):
        description = "alb -jucarie  -  patutul include:-1 perna - 2 plapumi" 
        
        result = DescriptionProcessor._MoveDashedLinesOnNewRow(description)
        expected = "alb <br />-jucarie  <br />-  patutul include:<br />-1 perna <br />- 2 plapumi"
        self.assertEqual(expected, result)
            

    def test__RemoveBreakAfterParagraphStart_BreakRemovalRequired_BreakRemoved(self):
        indata = "<p></br> - patut</p><p> </br>dummy text <p><br/>" 
        
        result = DescriptionProcessor._RemoveBreakAfterParagraphStart(indata)
        expected = "<p> - patut</p><p>dummy text <p>" 
        self.assertEqual(expected, result)

   
    def test_CleanDescription_HbbaInput(self):
        file = open("description_input_hbba.txt", "r")
        input = file.read()
        
        file = open("description_expected_hbba.txt", "r")
        expected = file.read()
        
        result = DescriptionProcessor.CleanDescription(input)
        print(result)
        #file = open("out.txt", "w")
        #file.write(result)
        #file.close()
        self.assertEqual(expected, result)
              

    def test_CleanDescription_NanInput(self):
        file = open("description_input_nan.txt", "r")
        input = file.read()
        
        file = open("description_expected_nan.txt", "r")
        expected = file.read()
        
        result = DescriptionProcessor.CleanDescription(input)
        print(result)
        self.assertEqual(expected, result)    
       
        
if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDescriptionProcessor)
    unittest.TextTestRunner(verbosity=2).run(suite)

