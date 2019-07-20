# -*- coding: utf-8 -*-
import General
import Data_Save
import time
import Options
import unittest
import json

class Test(unittest.TestCase):
    def test_Data_Save(self):
        Data_Save.reset()
        datas = Data_Save.get_all()

        # Test get_set(self):
        self.assertEqual(Data_Save.get("HGTD"), 0)
        Data_Save.set("HGTD", 10)
        self.assertEqual(Data_Save.get("HGTD"), 10)
        
        # Test add_scores/add_to_parameter
        self.assertEqual(Data_Save.get("total play"), 0)
        self.assertEqual(Data_Save.get("average time"), 0)
        Data_Save.add_scores([1000,500], 0.2)
        self.assertEqual(Data_Save.get("total play"), 2)
        self.assertEqual(Data_Save.get("average time"), 0.1)
        
        # Test get_time_hgtd/check_hgtd
        self.assertEqual(Data_Save.get_time_hgtd(), 0)
        self.assertEqual(Data_Save.check_hgtd(10000), True)
        time.sleep(1)
        self.assertTrue(Data_Save.get_time_hgtd() >= 1 and Data_Save.get_time_hgtd() < 2)
        Data_Save.reset()
        
    def test_Options(self):
        Options.reset()
        # Test get_all
        options = Options.get_all()
        
        # Test get/set
        Options.set("hardware", True)
        self.assertEqual(Options.get("hardware"), True)
        
        # Test ajout option inexistante via programmation
        self.assertRaises(AttributeError, lambda: Options.set("test", True)) 
        
        # Test ajout option inexistante via fichier de config json
        options["test"] = 10
        with open(Options.path, 'w') as options_file:
            json.dump(options, options_file, indent=2)
            
        self.assertRaises(AttributeError, lambda: Options.get("test"))
        Options.reset()
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   