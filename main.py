from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import shutil
import json
import os
from selenium.webdriver.common.by import By


# Setup for web scrap. Path needs to change for chromedriver.exe once uploaded in the cloud.
from selenium.webdriver.support.wait import WebDriverWait

driver_path = "./chromedriver.exe"

chrome_options = Options()
chrome_options.headless = True

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Starting website
driver.get("https://nutrition.sa.ucsc.edu/")

# Testing for sprint 2
# driver.get("https://nutrition.sa.ucsc.edu/label.aspx?locationNum=40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&dtdate=04%2f11%2f2022&RecNumAndPort=061003*1")


# Starting from the main dining hall page, the driver moves to the nutrition page for all the food of that dining hall
def moveToNutritionPage(dining_hall):

    driver.get("https://nutrition.sa.ucsc.edu/") #Resets the page incase url is different

    dining_hall_link = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.LINK_TEXT, dining_hall))
    dining_hall_link.click()

    nutrition_page = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.CLASS_NAME, "shortmenunutritive"))

    nutrition_page_link = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.LINK_TEXT, nutrition_page.text))

    nutrition_page_link.click()


# Given an list of all foods(Food genre and food names), parses it based on "--"
# Returns an dictionary

def splitAllFoods(lst, dining_hall):
    newLst = []

    current_food_type = None
    for i in lst:
        if i[0] == '-' and i[1] == '-':
            removeDash = len(i) - 3
            i = i[3:removeDash]
            current_food_type = i
            continue

        tmp = {
            'food_type': current_food_type,
            'food_name': i,
            'dining_hall': dining_hall
        }
        newLst.append(tmp)

    return newLst

# TODO: Sprint 2
# Starting from the food item nutrition page, all nutrition facts are scrapped
def singleNutritionFact(split_foods, count):
    nutrition_facts_table = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.XPATH, '//table[@bordercolorlight="#000000"]'))
    # print(nutrition_facts_table.text)
    food_name = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, 'labelrecipe'))
    #print(food_name.text)

    arr = nutrition_facts_table.text.split("\n")
    serving_size = arr[1]
    arr = arr[9:]
    arr.append(serving_size)
    # arr.append(food_name.text)
    for i in range(len(arr)):
        arr[i] = arr[i].lstrip()

    # split_foods[count]['total_fat'] = arr[0]
    # split_foods[count]['fat_dv'] = arr[1]
    # split_foods[count]['total_carb'] = arr[2]
    # split_foods[count]['carb_dv'] = arr[3]
    # split_foods[count]['saturated_fat'] = arr[4]
    # split_foods[count]['saturated_fat_dv'] = arr[5]
    # split_foods[count]['dietary_fiber'] = arr[6]
    # split_foods[count]['dietary_fiber_dv'] = arr[7]
    # split_foods[count]['trans_fat'] = arr[8]
    # split_foods[count]['sugar'] = arr[9]
    # split_foods[count]['cholestrol'] = arr[10]
    # split_foods[count]['cholestrol_dv'] = arr[11]
    # split_foods[count]['protein'] = arr[12]
    # split_foods[count]['sodium'] = arr[13]
    # split_foods[count]['sodium_dv'] = arr[14]
    # split_foods[count]['vitaminD'] = arr[15]
    # split_foods[count]['calcium'] = arr[16]
    # split_foods[count]['iron'] = arr[17]
    # split_foods[count]['potassium'] = arr[18]
    # split_foods[count]['serving_size'] = arr[19]
    # print(arr)


# Must call moveToNutritionPage() before calling this function.
# Scraps all information(food genre, name, nutrition facts,etc) and writes it to a JSON file

def getNutritionFacts(dining_hall):
    food_table = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@width="70%"]'))

    inner_table = WebDriverWait(food_table, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, 'table'))
    size = len(inner_table) - 1;

    all_foods = []
    for i in range(1, size, 2):
        try:
            getElement = inner_table[i].find_element(By.CLASS_NAME, "longmenucolmenucat")
            all_foods.append(getElement.text)
        except:
            getElement = inner_table[i].find_element(By.CLASS_NAME, "longmenucoldispname")
            all_foods.append(getElement.text)

    #print(all_foods)
    split_foods = splitAllFoods(all_foods, dining_hall)
    #print(split_foods)
    convertToJSON(split_foods, dining_hall)
    print("Webscrap " + dining_hall + " Successful")


    # CODE BELOW THIS POINT IS FOR SPRINT 2: SCRAPPING NUTRITION FACTS

    # for i in range(len(split_foods)):
    #     link = WebDriverWait(driver, timeout=3).until(
    #         lambda d: d.find_element(By.LINK_TEXT, split_foods[i]['food_name']))
    #     link.click()
    #     singleNutritionFact(split_foods, i)
    #     driver.back()

#Converts the list of dictionaries for split_foods into a JSON file based on the dining hall
def convertToJSON(split_foods, dining_hall):
    if dining_hall == 'College Nine/John R. Lewis Dining Hall':
        file_name = 'college_nine_john_lewis_dining.json'
    elif dining_hall == 'Cowell/Stevenson Dining Hall':
        file_name = 'cowell_stevenson_dining.json'
    elif dining_hall == 'Crown/Merrill Dining Hall':
        file_name = 'crown_merrill_dining.json'
    else:
        file_name = 'porter_kresge_dining.json'

    ofstrm = open(file_name, 'w')
    ofstrm.write('[\n')
    for i in split_foods:
        json.dump(i, ofstrm, indent=4)
        ofstrm.write(",\n")
    ofstrm.write('\n]')
    ofstrm.close()

    shutil.move('./' + file_name, './results')

#Removes the current JSON and replaces it with updated ones when the program ends
def removeCurrentJSON():
    if os.path.exists("./results/college_nine_john_lewis_dining.json"):
        os.remove("./results/college_nine_john_lewis_dining.json")

    if os.path.exists('./results/cowell_stevenson_dining.json'):
        os.remove('./results/cowell_stevenson_dining.json')

    if os.path.exists('./results/crown_merrill_dining.json'):
        os.remove('./results/crown_merrill_dining.json')

    if os.path.exists('./results/porter_kresge_dining.json'):
        os.remove('./results/porter_kresge_dining.json')


if __name__ == '__main__':
    dining_halls = ['College Nine/John R. Lewis Dining Hall', 'Cowell/Stevenson Dining Hall',
                    'Crown/Merrill Dining Hall', 'Porter/Kresge Dining Hall']

    removeCurrentJSON()


    for i in dining_halls:
        try:
            moveToNutritionPage(i)
            getNutritionFacts(i)
        except:
            print("Failed to extract a dining hall")
            continue

    # driver.get("https://nutrition.sa.ucsc.edu/")
    # time.sleep(1)
    driver.quit()
