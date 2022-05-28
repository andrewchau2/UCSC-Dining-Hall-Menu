from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sys import platform
import time
import shutil
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


###########################################################################################
# Selects the correct chromedriver to run depending on the OS
###########################################################################################

if platform == "darwin":
    driver_path = "./chromedriver"
    # OS X
elif platform == "win32":
    driver_path = "./chromedriver.exe"
    # Windows...
else:
    driver_path = "ERROR"

print(platform)

###########################################
# GLOBAL DRIVER OPTIONS AND PATH
# Current options applied: Hides pop-up for browser
###########################################
chrome_options = Options()
chrome_options.headless = True
service = Service(executable_path=driver_path)




class diningHallWebScrapper:
    def __init__(self):
        self.isFirstInput = True  # Used to ensure that first JSON entry of a food entry does not contain a , at the start
        self.all_foods = {}  # Contains all the food items with their properties
        self.switch_for_dining_hall = {
            'College Nine/John R. Lewis Dining Hall': 'clgnine_johnlewis',
            'Cowell/Stevenson Dining Hall': 'cowell_steve',
            'Crown/Merrill Dining Hall': 'crown_merill',
            'Porter/Kresge Dining Hall': 'porter_kresge'
        }
        self.dining_halls = ['College Nine/John R. Lewis Dining Hall', 'Cowell/Stevenson Dining Hall',
                    'Crown/Merrill Dining Hall', 'Porter/Kresge Dining Hall']


        ###########################################################################################
        # Setup for the Webscrapper.
        # Sets start page to https://nutrition.sa.ucsc.edu/
        ###########################################################################################

        global service
        #self.driver = webdriver.Chrome(service=service, options=chrome_options) #Comment if (driver = ...) is uncommented
        self.driver = webdriver.Chrome(service=service) #Uncomment to see browser

        self.driver.get("https://nutrition.sa.ucsc.edu/")  # Starting website

    def getDiningHallUrl(self):
        return self.driver.current_url

    def startDiningHallScrapper(self):

        for curr_dining_hall in self.dining_halls:
            try:
                self.moveToNutritionPage(curr_dining_hall)
                self.webScrapAllMealsTimes(curr_dining_hall)
            except:
                print("Failed to extract " + curr_dining_hall + " dining hall")
                continue

        print("Total menu items scrapped: ", str(len(self.all_foods)))
        # driver.get("https://nutrition.sa.ucsc.edu/")
        self.endDiningHallScrapper()

    def endDiningHallScrapper(self):
        self.driver.quit()

    def createFoodResultsJson(self):
        try:
            self.removeCurrentJSON()
            self.convertToJSON(self.all_foods)
            self.moveToResultsFolder()
            return True
        except:
            return False

    def checkFoodResultsPath(self):
        if os.path.exists("./results/food_results.json"):
            return True
        return False

    def removeCurrentJSON(self):
        if self.checkFoodResultsPath():
            os.remove("./results/food_results.json")

    def moveToResultsFolder(self):
        shutil.move('./food_results.json', './results')

    # Converts the list of dictionaries for split_foods into a JSON file based on the dining hall
    def convertToJSON(self,all_foods):
        file_name = "./food_results.json"
        ofstrm = open(file_name, 'w+')
        size = len(all_foods)
        count = 0

        ofstrm.write('[\n')
        if self.isFirstInput:
            self.isFirstInput = False
        else:
            ofstrm.write(",")
        for key, value in all_foods.items():
            json.dump(value, ofstrm, indent=4)
            count += 1
            if count == size:
                ofstrm.write("\n")
            if count != size:
                ofstrm.write(",\n")
        ofstrm.write(']')
        ofstrm.close()

    def resetDiningHallPage(self):
        self.driver.get("https://nutrition.sa.ucsc.edu/")  # Resets the page incase url is different

    # Starting from the main dining hall page, the driver moves to the nutrition page for all the food of that dining hall
    def moveToNutritionPage(self,dining_hall):
        try:
            self.resetDiningHallPage()

            dining_hall_link = WebDriverWait(self.driver, timeout=3).until(
                lambda d: d.find_element(By.LINK_TEXT, dining_hall))
            dining_hall_link.click()
            return True
        except:
            return False

    def __getMealTimeLinks(self):
        # Setup: Obtaining len and name of meal times(Breakfast, Lunch, Dinner, Late_Night)
        nutrition_pages = WebDriverWait(self.driver, timeout=3).until(
            lambda d: d.find_elements(By.CLASS_NAME, "shortmenunutritive"))

        meal_time_elems = WebDriverWait(self.driver, timeout=3).until(
            lambda d: d.find_elements(By.CLASS_NAME, "shortmenumeals"))

        meal_times = []
        for meal_time in meal_time_elems:
            meal_times.append(meal_time.text)
        return meal_times

    # Calls each meal time for the specific dining hall and then calls getNutritionFacts() to start scrapping all the data
    def webScrapAllMealsTimes(self,dining_hall):
        try:
            # Setup: Obtaining len and name of meal times(Breakfast, Lunch, Dinner, Late_Night)
            meal_times = self.__getMealTimeLinks()
            total_meal_times = len(meal_times)

            # Webscrapper starts below this point using the data from setup:
            for curr_meal_type in range(total_meal_times):
                nutrition_pages = WebDriverWait(self.driver, timeout=3).until(
                    lambda d: d.find_elements(By.CLASS_NAME, "shortmenunutritive"))
                nutrition_pages[curr_meal_type].click()
                curr_meal_time = meal_times[curr_meal_type]
                if curr_meal_time == 'Late Night':  # Changed to Late_Night to avoid space conflicts
                    curr_meal_time = 'Late_Night'
                self.__getNutritionFacts(dining_hall, curr_meal_time)
            return True
        except:
            return False

    def __getFoodType(self, raw_food_type_text):
        REMOVE_FRONT_DASH = 3
        REMOVE_BACK_DASH = len(raw_food_type_text) - 3
        parsed_food_type = raw_food_type_text[REMOVE_FRONT_DASH:REMOVE_BACK_DASH]
        return parsed_food_type

    def __init_basic_food_obj(self,current_food_type,food_name):
        food_obj = {
            'food_type': current_food_type,
            'food_name': food_name,
            'dining_hall': {
                'clgnine_johnlewis': False,
                'cowell_steve': False,
                'crown_merill': False,
                'porter_kresge': False
            },
            'meal_time': {
                'Breakfast': False,
                'Lunch': False,
                'Dinner': False,
                'Late_Night': False
            }
        }
        self.all_foods[food_name] = food_obj
        return food_obj


    ###########################################################################################
    # Get functions for all nutrient/tag info about a specific food item
    # All get functions are called within singleNutrientFacts()
    ###########################################################################################

    # Used as an helper for the getter functions. Returns elem based on XPATH given
    def __searchNutritionFactBoxHTML(self,xpath_val):
        try:
            result_elem = WebDriverWait(self.driver, timeout=0.5).until(
                lambda d: d.find_element(By.XPATH, xpath_val))
            return result_elem.text.lstrip()
        except:
            return None

    def __getServing_size(self,curr_food_obj):
        curr_food_obj['serving_size'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[1]/td[1]/font[3]')

    def __getCalories(self,curr_food_obj):
        try:
            calories_text = WebDriverWait(self.driver, timeout=0.5).until(
                lambda d: d.find_element(By.XPATH, '/html/body/table[1]/tbody/tr/td/table/tbody/tr[1]/td[1]/font[4]'))

            calories_arr = calories_text.text.split(' ')

            NO_CALORIES_FOUND_BEYOND_2 = 2

            if len(calories_arr) < NO_CALORIES_FOUND_BEYOND_2:  # No Calories value
                curr_food_obj['calories'] = None
            else:
                curr_food_obj['calories'] = calories_arr[1]
        except:
            curr_food_obj['calories'] = None

    def __getTotalFat(self,curr_food_obj):
        curr_food_obj['total_fat'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[1]/font[2]')

    def __getTotalFat_DV(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[2]/font[1]/b')
        curr_food_obj['total_fat_DV'] = None if result == '' else result

    def __getSatFat(self,curr_food_obj):
        curr_food_obj['sat_fat'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[1]/font[2]')

    def __getSatFat_DV(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/font[1]/b')
        curr_food_obj['sat_fat_DV'] = None if result == '' else result

    def __getTransFat(self,curr_food_obj):
        curr_food_obj['trans_fat'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[4]/td[1]/font[2]')

    def __getCholesterol(self,curr_food_obj):
        curr_food_obj['cholesterol'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[5]/td[1]/font[2]')

    def __getCholesterol_DV(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[5]/td[2]/font[1]/b')
        curr_food_obj['cholesterol_DV'] = None if result == '' else result

    def __getSodium(self,curr_food_obj):
        curr_food_obj['sodium'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[6]/td[1]/font[2]')

    def __getSodiumDV(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[6]/td[2]/font[1]/b')
        curr_food_obj['sodium_DV'] = None if result == '' else result

    def __getTotalCarbs(self,curr_food_obj):
        curr_food_obj['total_carbs'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[3]/font[2]')

    def __getTotalCarbs_DV(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[4]/font[1]/b')
        curr_food_obj['total_carbs_DV'] = None if result == '' else result

    def __getDietaryFiber(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[3]/font[2]')
        curr_food_obj['dietary_fiber'] = '- - - g' if result is None else result

    def __getDietaryFiber_DV(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[4]/font[1]/b')
        curr_food_obj['dietary_fiber_DV'] = None if result == '' else result

    def __getSugars(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[4]/td[3]/font[2]')
        curr_food_obj['sugars'] = '- - - g' if result is None else result

    def __getProtein(self,curr_food_obj):
        curr_food_obj['protein'] = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[5]/td[3]/font[2]')

    def __getIngredients(self,curr_food_obj):
        curr_food_obj['ingredients'] = self.__searchNutritionFactBoxHTML('/html/body/table[2]/tbody/tr/td/span[2]')

    def __getAllergens(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML('/html/body/table[3]/tbody/tr/td/span[2]')
        curr_food_obj['allergens'] = None if result == '' else result

    def __getVitamin_D(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[1]/table/tbody/tr/td/font[2]')
        curr_food_obj['vitamin_d'] = None if result == '' else result

    def __getCalcium(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[2]/table/tbody/tr/td/li/font[2]')
        curr_food_obj['calcium'] = None if result == '' else result

    def __getIron(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[3]/table/tbody/tr/td/li/font[2]')
        curr_food_obj['iron'] = None if result == '' else result

    def __getPotassium(self,curr_food_obj):
        result = self.__searchNutritionFactBoxHTML(
            '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[4]/table/tbody/tr/td/li/font[2]')
        curr_food_obj['potassium'] = None if result == '' else result

    def __getFoodTags(self,curr_food_obj):
        tmp = {
            'Eggs': False,
            'Fish': False,
            'GlutenFree': False,
            'Dairy': False,
            'Peanuts': False,
            'Soy': False,
            'Vegan': False,
            'Vegetarian': False,
            'Pork': False,
            'Beef': False,
            'Halal': False,
            'Shellfish': False,
            'TreeNut': False

        }

        try:
            food_tag_elem = WebDriverWait(self.driver, timeout=0.5).until(
                lambda d: d.find_element(By.CLASS_NAME, 'labelwebcodesvalue'))

            all_tags = WebDriverWait(food_tag_elem, timeout=0.5).until(
                lambda d: d.find_elements(By.TAG_NAME, 'img'))

            curr_food_obj['food_tags'] = {

            }

            for curr_tag in all_tags:
                curr_tag_text = curr_tag.get_attribute('alt')
                if curr_tag_text == 'Egg/s':  # Egg/s changed to Eggs to avoid a possible URL path issue
                    tmp['Eggs'] = True
                elif curr_tag_text == 'Gluten Free' or curr_tag_text == 'Gluten-Free':
                    tmp['GlutenFree'] = True
                elif curr_tag_text == 'Tree Nut':
                    tmp['TreeNut'] = True
                else:
                    tmp[curr_tag_text] = True

            curr_food_obj['food_tags'] = tmp
        except:
            curr_food_obj['food_tags'] = tmp

    # Starting from the food item nutrition page, all nutrition facts are scrapped
    def singleNutritionFact(self,curr_food_obj):
        self.__getServing_size(curr_food_obj)
        self.__getCalories(curr_food_obj)
        self.__getTotalFat(curr_food_obj)
        self.__getSatFat(curr_food_obj)
        self.__getTransFat(curr_food_obj)
        self.__getCholesterol(curr_food_obj)
        self.__getSodium(curr_food_obj)
        self.__getTotalCarbs(curr_food_obj)
        self.__getDietaryFiber(curr_food_obj)
        self.__getSugars(curr_food_obj)
        self.__getProtein(curr_food_obj)
        self.__getIngredients(curr_food_obj)
        self.__getAllergens(curr_food_obj)
        self.__getVitamin_D(curr_food_obj)
        self.__getCalcium(curr_food_obj)
        self.__getIron(curr_food_obj)
        self.__getPotassium(curr_food_obj)
        self.__getFoodTags(curr_food_obj)
        self.__getTotalFat_DV(curr_food_obj)
        self.__getSatFat_DV(curr_food_obj)
        self.__getCholesterol_DV(curr_food_obj)
        self.__getSodiumDV(curr_food_obj)
        self.__getTotalCarbs_DV(curr_food_obj)
        self.__getDietaryFiber_DV(curr_food_obj)

    def __start_nutrient_fact_webscrapper(self, curr_foods):
        # Gets the nutrient facts for all food items that have just recently been added to all_foods{}.
        # Recent food names are in curr_foods[]
        for count in range(len(curr_foods)):
            link = WebDriverWait(self.driver, timeout=3).until(
                lambda d: d.find_element(By.LINK_TEXT, curr_foods[count]['food_name']))
            link.click()
            self.singleNutritionFact(curr_foods[count])
            self.driver.back()  # Returns to list of meal time page

    # Must call moveToNutritionPage() before calling this function.
    # Scraps all information(food genre, name, nutrition facts,etc) and writes it to a JSON file

    def __getNutritionFacts(self,dining_hall, meal_time):
        food_table = WebDriverWait(self.driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@width="70%"]'))

        inner_table = WebDriverWait(food_table, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, 'table'))
        size = len(inner_table) - 1

        current_food_type = ''
        curr_foods = []
        for i in range(1, size, 2):
            try:
                try:  # Result is the food type. Parses the string and sets current_food_type
                    raw_food_type = inner_table[i].find_element(By.CLASS_NAME, "longmenucolmenucat")
                    current_food_type = self.__getFoodType(raw_food_type.text)

                except:  # Result is the food name. Checks if food_name is in all_foods{}.
                    # If not, create new obj with default parameters. Else update the object.
                    food_name = inner_table[i].find_element(By.CLASS_NAME, "longmenucoldispname")
                    food_obj = self.all_foods.get(food_name.text)
                    if food_obj is None:
                        food_obj = self.__init_basic_food_obj(current_food_type,food_name.text)
                        curr_foods.append(food_obj)
                    set_dining_hall = self.switch_for_dining_hall.get(dining_hall)
                    food_obj['dining_hall'][set_dining_hall] = True
                    food_obj['meal_time'][meal_time] = True
            except:
                print("FATAL ERROR: FOOD NAMES PARSED INCORRECTLY")

        self.__start_nutrient_fact_webscrapper(curr_foods)

        print("Webscrap " + dining_hall + ": " + meal_time + " Successful")
        self.driver.back()  # Returns back to dining hall's food list page