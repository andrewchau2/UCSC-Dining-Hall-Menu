from selenium import webdriver
# from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
import time
import json
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Setup for web scrap. Path needs to change for chromedriver.exe once uploaded in the cloud.
from selenium.webdriver.support.wait import WebDriverWait

driver_path = "C:\Program Files (x86)\chromedriver.exe"
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# Starting website
driver.get("https://nutrition.sa.ucsc.edu/")
#driver.get("https://nutrition.sa.ucsc.edu/label.aspx?locationNum=40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&dtdate=04%2f11%2f2022&RecNumAndPort=061003*1")


# Starting from the main dining hall page, the driver moves to the nutrition page for all the food of that dining hall
# driver.current_url MUST BE https://nutrition.sa.ucsc.edu/
def moveToNutritionPage(dining_hall):
    # dining_location = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, "locations"))
    # print(dining_location.text)
    driver.get("https://nutrition.sa.ucsc.edu/")

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
            current_food_type = i
            continue

        tmp = {
            'food_type' : current_food_type,
            'food_name' : i,
            'dining_hall' : dining_hall
        }
        newLst.append(tmp)

    return newLst

# Starting from the food item nutrition page, all nutrition facts are scrapped
def singleNutritionFact(split_foods, count):
    nutrition_facts_table = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@bordercolorlight="#000000"]'))
    #print(nutrition_facts_table.text)
    food_name = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, 'labelrecipe'))
    print(food_name.text)

    arr = nutrition_facts_table.text.split("\n")
    serving_size = arr[1]
    arr = arr[9:]
    arr.append(serving_size)
    #arr.append(food_name.text)
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
    #print(arr)



# Must call moveToNutritionPage() before calling this function.

def getNutritionFacts(dining_hall):
    food_table = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@width="70%"]'))
   # print(food_table.get_attribute("innerHTML"))

    inner_table = WebDriverWait(food_table, timeout=3).until(lambda d: d.find_elements(By.TAG_NAME, 'table'))
    size = len(inner_table) - 1;
    # print(len(inner_table))
    # print(inner_table[1].get_attribute("innerHTML"))
    all_foods = []
    for i in range(1, size, 2):
        try:
            getElement = inner_table[i].find_element(By.CLASS_NAME, "longmenucolmenucat")
            #all_foods.append("--") #Placeholder to track start of each genre
            all_foods.append(getElement.text)
        except:
            getElement = inner_table[i].find_element(By.CLASS_NAME, "longmenucoldispname")
            all_foods.append(getElement.text)

    print(all_foods)
    split_foods = splitAllFoods(all_foods, dining_hall)
    print(split_foods)

    for i in range(len(split_foods)):
        link = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.LINK_TEXT, split_foods[i]['food_name']))
        link.click()
        singleNutritionFact(split_foods, i)
        driver.back()
        # for j in range(1,len(split_foods[i])):
        #     link = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.LINK_TEXT, split_foods[i][j]))
        #     link.click()
        #     singleNutritionFact()
        #     driver.back()

    print(split_foods[0])


if __name__ == '__main__':
    dining_halls = ['College Nine/John R. Lewis Dining Hall','Cowell/Stevenson Dining Hall','Crown/Merrill Dining Hall','Porter/Kresge Dining Hall']

    for i in dining_halls:
        moveToNutritionPage(i)
        getNutritionFacts(i)
    #singleNutritionFact()
    driver.get("https://nutrition.sa.ucsc.edu/")
    time.sleep(1)
    driver.quit()
