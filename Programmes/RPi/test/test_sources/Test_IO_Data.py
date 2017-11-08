# -*- coding: utf-8 -*-
import General
import Data_Save
import time
import Options
import unittest
import json

class Test(unittest.TestCase):
    def test_Data_Save(self):
        Data_Save.reset_data()
        datas = Data_Save.get_all_data()

        # Test get_data_set_data(self):
        Data_Save.set_data("HGTD", 10)
        self.assertEqual(Data_Save.get_data("HGTD"), 10)
        
        # Test add_scores/add_to_parameter
        Data_Save.add_scores([1000,500], 0.2)
        self.assertEqual(Data_Save.get_data("average score"), 750)
        self.assertEqual(Data_Save.get_data("total play"), 2)
        self.assertEqual(Data_Save.get_data("average time"), 0.1)
        
        # Test get_time_hgtd/check_hgtd
        self.assertEqual(Data_Save.get_time_hgtd(), 0)
        self.assertEqual(Data_Save.check_hgtd(10000), True)
        time.sleep(1)
        self.assertTrue(Data_Save.get_time_hgtd() >= 1 and Data_Save.get_time_hgtd() < 2)
        Data_Save.reset_data()
        
    def test_Options(self):
        Options.reset_options()
        # Test get_all_data
        options = Options.get_all_options()
        
        # Test get_option/set_option
        Options.set_option("hardware", True)
        self.assertEqual(Options.get_option("hardware"), True)
        
        # Test ajout option inexistante via programmation
        self.assertRaises(AttributeError, lambda: Options.set_option("test", True)) 
        
        # Test ajout option inexistante via fichier de config json
        options["test"] = 10
        with open(Options.path, 'w') as options_file:
            json.dump(options, options_file, indent=2)
            
        self.assertRaises(AttributeError, lambda: Options.get_option("test"))
        Options.reset_options()
        
####################################################################################################################################

if __name__ == "__main__": 
    unittest.main()   