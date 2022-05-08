from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sys import platform
import time
import shutil
import json
import os
from selenium.webdriver.common.by import By

###########################################################################################
# Selects the correct chromedriver to run depending on the OS
###########################################################################################
from selenium.webdriver.support.wait import WebDriverWait

if platform == "darwin":
    driver_path = "./chromedriver"
    # OS X
elif platform == "win32":
    driver_path = "./chromedriver.exe"
    # Windows...
else:
    driver_path = "ERROR"

print(platform)

###########################################################################################
# Setup for the Webscrapper.
# Sets start page to https://nutrition.sa.ucsc.edu/
# Current options applied: Hides pop-up for browser
###########################################################################################

chrome_options = Options()
# chrome_options.headless = True

service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome(service=service)

driver.get("https://nutrition.sa.ucsc.edu/")  # Starting website


###########################################################################################
# Get functions for all nutrient/tag info about a specific food item
# All get functions are called within singleNutrientFacts()
###########################################################################################

def searchNutritionFactBoxHTML(xpath_val):
    try:
        result_elem = WebDriverWait(driver, timeout=1).until(
            lambda d: d.find_element(By.XPATH, xpath_val))
        return result_elem.text.lstrip()
    except:
        return None


def getServing_size(split_foods, count):
    split_foods[count]['serving_size'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[1]/td[1]/font[3]')


def getCalories(split_foods, count):
    try:
        calories_text = WebDriverWait(driver, timeout=1).until(
            lambda d: d.find_element(By.XPATH, '/html/body/table[1]/tbody/tr/td/table/tbody/tr[1]/td[1]/font[4]'))

        calories_arr = calories_text.text.split(' ')

        NO_CALORIES_FOUND_BEYOND_2 = 2

        if len(calories_arr) < NO_CALORIES_FOUND_BEYOND_2:  # No Calories value
            split_foods[count]['calories'] = None
        else:
            split_foods[count]['calories'] = calories_arr[1]
    except:
        split_foods[count]['calories'] = None


def getTotalFat(split_foods, count):
    split_foods[count]['total_fat'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[1]/font[2]')


def getTotalFat_DV(split_foods, count):
    split_foods[count]['total_fat_DV'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[2]/font[1]/b')


def getSatFat(split_foods, count):
    split_foods[count]['sat_fat'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[1]/font[2]')


def getSatFat_DV(split_foods, count):
    split_foods[count]['sat_fat_DV'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/font[1]/b')


def getTransFat(split_foods, count):
    split_foods[count]['trans_fat'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[4]/td[1]/font[2]')


def getCholesterol(split_foods, count):
    split_foods[count]['cholesterol'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[5]/td[1]/font[2]')


def getCholesterol_DV(split_foods, count):
    split_foods[count]['cholesterol_DV'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[5]/td[2]/font[1]/b')


def getSodium(split_foods, count):
    split_foods[count]['sodium'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[6]/td[1]/font[2]')


def getSodiumDV(split_foods, count):
    split_foods[count]['sodium_DV'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[6]/td[2]/font[1]/b')


def getTotalCarbs(split_foods, count):
    split_foods[count]['total_carbs'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[3]/font[2]')


def getTotalCarbs_DV(split_foods, count):
    split_foods[count]['total_carbs_DV'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[2]/td[4]/font[1]/b')


def getDietaryFiber(split_foods, count):
    split_foods[count]['dietary_fiber'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[3]/font[2]')


def getDietaryFiber_DV(split_foods, count):
    split_foods[count]['dietary_fiber_DV'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td[4]/font[1]/b')


def getSugars(split_foods, count):
    split_foods[count]['sugars'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[4]/td[3]/font[2]')


def getProtein(split_foods, count):
    split_foods[count]['protein'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[5]/td[3]/font[2]')


def getIngredients(split_foods, count):
    split_foods[count]['ingredients'] = searchNutritionFactBoxHTML('/html/body/table[2]/tbody/tr/td/span[2]')


def getAllergens(split_foods, count):
    split_foods[count]['allergens'] = searchNutritionFactBoxHTML('/html/body/table[3]/tbody/tr/td/span[2]')


def getVitamin_D(split_foods, count):
    split_foods[count]['vitamin_d'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[1]/table/tbody/tr/td/font[2]')


def getCalcium(split_foods, count):
    split_foods[count]['calcium'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[2]/table/tbody/tr/td/li/font[2]')


def getIron(split_foods, count):
    split_foods[count]['iron'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[3]/table/tbody/tr/td/li/font[2]')


def getPotassium(split_foods, count):
    split_foods[count]['potassium'] = searchNutritionFactBoxHTML(
        '/html/body/table[1]/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td[4]/table/tbody/tr/td/li/font[2]')


def getFoodTags(split_foods, count):
    try:
        food_tag_elem = WebDriverWait(driver, timeout=1).until(
            lambda d: d.find_element(By.CLASS_NAME, 'labelwebcodesvalue'))

        all_tags = WebDriverWait(food_tag_elem, timeout=1).until(
            lambda d: d.find_elements(By.TAG_NAME, 'img'))

        split_foods[count]['food_tags'] = {

        }
        tmp = {
            'Eggs': False,
            'Fish': False,
            'Gluten-Free': False,
            'Dairy': False,
            'Peanuts': False,
            'Soy': False,
            'Vegan': False,
            'Vegetarian': False,
            'Pork': False,
            'Beef': False,
            'Halal': False,
            'Shellfish': False,
            'Tree Nut': False

        }

        for curr_tag in all_tags:
            curr_tag_text = curr_tag.get_attribute('alt')
            if curr_tag_text == 'Egg/s':
                tmp['Eggs'] = True
            else:
                tmp[curr_tag_text] = True

        split_foods[count]['food_tags'] = tmp
    except:
        split_foods[count]['food_tags'] = []


# Starting from the food item nutrition page, all nutrition facts are scrapped
def singleNutritionFact(split_foods, count):
    getServing_size(split_foods, count)
    getCalories(split_foods, count)
    getTotalFat(split_foods, count)
    getSatFat(split_foods, count)
    getTransFat(split_foods, count)
    getCholesterol(split_foods, count)
    getSodium(split_foods, count)
    getTotalCarbs(split_foods, count)
    getDietaryFiber(split_foods, count)
    getSugars(split_foods, count)
    getProtein(split_foods, count)
    getIngredients(split_foods, count)
    getAllergens(split_foods, count)
    getVitamin_D(split_foods, count)
    getCalcium(split_foods, count)
    getIron(split_foods, count)
    getPotassium(split_foods, count)
    getFoodTags(split_foods, count)
    getTotalFat_DV(split_foods, count)
    getSatFat_DV(split_foods, count)
    getCholesterol_DV(split_foods, count)
    getSodiumDV(split_foods, count)
    getTotalCarbs_DV(split_foods, count)
    getDietaryFiber_DV(split_foods, count)


###########################################################################################
# Starts the process of getting and storing food info into JSON.
###########################################################################################

# GLOBAL VARIABLES:
isFirstInput = True  # Used to ensure that first JSON entry of a food entry does not contain a , at the start
all_foods = {}  # Contains all the food items with their properties
switch_for_dining_hall = {
    'College Nine/John R. Lewis Dining Hall': 'clgnine_johnlewis',
    'Cowell/Stevenson Dining Hall': 'cowell_steve',
    'Crown/Merrill Dining Hall': 'crown_merill',
    'Porter/Kresge Dining Hall': 'porter_kresge'
}


# Starting from the main dining hall page, the driver moves to the nutrition page for all the food of that dining hall
def moveToNutritionPage(dining_hall):
    driver.get("https://nutrition.sa.ucsc.edu/")  # Resets the page incase url is different

    dining_hall_link = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.LINK_TEXT, dining_hall))
    dining_hall_link.click()


def webScrapAllMealsTimes(dining_hall):
    nutrition_pages = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_elements(By.CLASS_NAME, "shortmenunutritive"))

    meal_time_elems = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_elements(By.CLASS_NAME, "shortmenumeals"))

    meal_times = []
    for meal_time in meal_time_elems:
        meal_times.append(meal_time.text)
    total_meal_types = len(nutrition_pages)

    for curr_meal_type in range(total_meal_types):
        nutrition_pages = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_elements(By.CLASS_NAME, "shortmenunutritive"))
        nutrition_pages[curr_meal_type].click()
        curr_meal_time = meal_times[curr_meal_type]
        if curr_meal_time == 'Late Night':
            curr_meal_time = 'Late_Night'
        getNutritionFacts(dining_hall, curr_meal_time)


# Must call moveToNutritionPage() before calling this function.
# Scraps all information(food genre, name, nutrition facts,etc) and writes it to a JSON file

def getNutritionFacts(dining_hall, meal_time):
    global switch_for_dining_hall
    food_table = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@width="70%"]'))

    inner_table = WebDriverWait(food_table, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, 'table'))
    size = len(inner_table) - 1

    current_food_type = ''
    curr_foods = []
    for i in range(1, size, 2):
        try:
            try:
                raw_food_type = inner_table[i].find_element(By.CLASS_NAME, "longmenucolmenucat")
                REMOVE_FRONT_DASH = 3
                REMOVE_BACK_DASH = len(raw_food_type.text) - 3
                parsed_food_type = raw_food_type.text[REMOVE_FRONT_DASH:REMOVE_BACK_DASH]
                current_food_type = parsed_food_type


            except:
                food_name = inner_table[i].find_element(By.CLASS_NAME, "longmenucoldispname")
                food_obj = all_foods.get(food_name.text)
                if food_obj is None:
                    tmp = {
                        'food_type': current_food_type,
                        'food_name': food_name.text,
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
                    food_obj = tmp
                    all_foods[food_name.text] = tmp
                    curr_foods.append(tmp)

                set_dining_hall = switch_for_dining_hall.get(dining_hall)
                food_obj['dining_hall'][set_dining_hall] = True
                food_obj['meal_time'][meal_time] = True
        except:
            print("FATAL ERROR: FOOD NAMES PARSED INCORRECTLY")

    for count in range(len(curr_foods)):
        link = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element(By.LINK_TEXT, curr_foods[count]['food_name']))
        link.click()
        singleNutritionFact(curr_foods, count)
        driver.back()

    print("Webscrap " + dining_hall + ": " + meal_time + " Successful")
    driver.back()


# Converts the list of dictionaries for split_foods into a JSON file based on the dining hall
def convertToJSON():
    global all_foods
    file_name = "food_results.json"
    ofstrm = open(file_name, 'a+')
    size = len(all_foods)
    count = 0
    global isFirstInput

    if isFirstInput:
        isFirstInput = False
    else:
        ofstrm.write(",")
    for key, value in all_foods.items():
        json.dump(value, ofstrm, indent=4)
        count += 1
        if count == size:
            ofstrm.write("\n")
        if count != size:
            ofstrm.write(",\n")
    ofstrm.close()


###########################################################################################
# Calls the webscrapper to get food info from all 4 dining halls.
# Deletes existing food_results.json and starts creating a new one.
###########################################################################################

# Removes the current JSON and replaces it with updated ones when the program ends
def removeCurrentJSON():
    if os.path.exists("./results/food_results.json"):
        os.remove("./results/food_results.json")


if __name__ == '__main__':
    start_time = time.time()
    dining_halls = ['College Nine/John R. Lewis Dining Hall', 'Cowell/Stevenson Dining Hall',
                    'Crown/Merrill Dining Hall', 'Porter/Kresge Dining Hall']

    removeCurrentJSON()
    with open('food_results.json', 'a+') as op:
        op.write('[\n')
    # moveToNutritionPage(dining_halls[0])
    # webScrapAllMealsTimes(dining_halls[0])
    for curr_dining_hall in dining_halls:
        try:
            moveToNutritionPage(curr_dining_hall)
            webScrapAllMealsTimes(curr_dining_hall)
        except:
            print("Failed to extract " + curr_dining_hall + " dining hall")
            continue

    print("Total menu items scrapped: ", str(len(all_foods)))
    convertToJSON()
    with open('food_results.json', 'a+') as op:
        op.write(']')
    shutil.move('./food_results.json', './results')

    # driver.get("https://nutrition.sa.ucsc.edu/")
    driver.quit()
    finish_time = time.time()
    print("Runtime:", str((finish_time - start_time) / 60.0), "minutes")
