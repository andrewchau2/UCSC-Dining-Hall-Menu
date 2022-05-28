import unittest
import diningHallScrapper
import random
import json
import shutil
import os

class TestDHScrapper(unittest.TestCase):
    def setUp(self):
        self.dhScrapper = diningHallScrapper.diningHallWebScrapper()
        self.dining_halls = ['College Nine/John R. Lewis Dining Hall', 'Cowell/Stevenson Dining Hall',
                             'Crown/Merrill Dining Hall', 'Porter/Kresge Dining Hall']

    def tearDown(self):
        self.dhScrapper.endDiningHallScrapper()

    def test_resetDiningHallPage_ShouldBeUCSCDiningHallWebsite(self):
        self.dhScrapper.resetDiningHallPage()
        result = self.dhScrapper.getDiningHallUrl()
        self.assertEqual(result,'https://nutrition.sa.ucsc.edu/')

    def test_moveToNutrientPage_ShouldBeTrue(self):
        for i in self.dining_halls:
            self.dhScrapper.resetDiningHallPage()
            result = self.dhScrapper.moveToNutritionPage(i)
            self.assertEqual(result, True)

    def test_webScrapAllMealsTimes_ShouldBeTrue(self):
        selected_dining_hall = self.dining_halls[random.randrange(0,4)]
        self.dhScrapper.resetDiningHallPage()
        self.dhScrapper.moveToNutritionPage(selected_dining_hall)
        result = self.dhScrapper.webScrapAllMealsTimes(selected_dining_hall)
        self.assertEqual(result, True)

    def checkFoodInfoLength_ShouldBeTrue(self,food_item):
        total_food_parameters = 28
        self.assertEqual(len(food_item),total_food_parameters)

    def checkFoodFacts_ShouldBeTrue(self,food_keys,food_item):
        for curr_food_key in food_keys:
            if curr_food_key not in food_item:
                print(curr_food_key)
                print("Here")
                return False
        return True

    def test_webScrappedFoodInfo_ShouldBeTrue(self):
        pathExists = self.dhScrapper.checkFoodResultsPath()
        if pathExists is False:
            self.assertEqual(pathExists, True)

        food_keys = ['food_type', 'food_name','serving_size','calories','total_fat','sat_fat',
                'trans_fat','cholesterol','sodium','total_carbs','dietary_fiber','sugars',
                'protein','ingredients','allergens','vitamin_d','calcium','iron','potassium',
                'total_fat_DV','sat_fat_DV','cholesterol_DV','sodium_DV','total_carbs_DV','dietary_fiber_DV',
                'meal_time','dining_hall','food_tags']

        ofstrm = open('./results/food_results.json')
        food_data = json.loads(ofstrm.read())
        ofstrm.close()

        for curr_food_data in food_data:
            self.checkFoodInfoLength_ShouldBeTrue(curr_food_data)
            result = self.checkFoodFacts_ShouldBeTrue(food_keys,curr_food_data)
            self.assertEqual(result,True)



class TestDHFoodResults(unittest.TestCase):
    def setUp(self):
        self.dhScrapper = diningHallScrapper.diningHallWebScrapper()

    def tearDown(self):
        self.dhScrapper.endDiningHallScrapper()

    def test_checkFoodResultsPath_ShouldBeTrue(self):
        result = self.dhScrapper.checkFoodResultsPath()
        self.assertEqual(result, True)

    def test_createFoodResultsJson_ShouldBeTrue(self):
        result = self.dhScrapper.checkFoodResultsPath()
        if result:
            path = "./results/food_results.json"
            shutil.copyfile(path, './tmp.json')

            result = self.dhScrapper.createFoodResultsJson() #Unit test

            # #Restoring preserved data
            self.dhScrapper.removeCurrentJSON()
            os.rename('./tmp.json', './food_results.json')
            try:
                self.dhScrapper.moveToResultsFolder()
            except shutil.SameFileError:
                pass
        self.assertEqual(result, True)



if __name__ == '__main__':
    unittest.main()



