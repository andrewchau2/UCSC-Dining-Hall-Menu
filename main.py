from selenium import webdriver
# from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
import time
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


def moveToNutritionPage():
    dining_location = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, "locations"))
    print(dining_location.text)

    dining_hall_link = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.LINK_TEXT, dining_location.text))
    dining_hall_link.click()

    nutrition_page = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.CLASS_NAME, "shortmenunutritive"))

    nutrition_page_link = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(By.LINK_TEXT, nutrition_page.text))

    nutrition_page_link.click()


def splitAllFoods(lst):
    newLst = []
    tmp = []

    for i in lst:
        if i == '--':
            newLst.append(tmp)
            tmp = []
            continue
        tmp.append(i)
    newLst.append(tmp) #Last one

    return newLst



def singleNutritionFact():
    nutrition_facts_table = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@bordercolorlight="#000000"]'))
    #print(nutrition_facts_table.text)
    food_name = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, 'labelrecipe'))
    print(food_name.text)
    arr = nutrition_facts_table.text.split("\n")
    serving_size = arr[1]
    arr = arr[9:]
    arr.append(serving_size)
    arr.append(food_name.text)
    for i in range(len(arr)):
        arr[i] = arr[i].lstrip()
    print(arr)



# Must call moveToNutritionPage() before calling this function.
# Driver current_url should be similar to:
# https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&naFlag=1&WeeksMenus=UCSC+-+This+Week%27s+Menus&dtdate=04%2f08%2f2022&mealName=Breakfast
def getNutritionFacts():
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
            all_foods.append("--")
            all_foods.append(getElement.text)
        except:
            getElement = inner_table[i].find_element(By.CLASS_NAME, "longmenucoldispname")
            all_foods.append(getElement.text)

    all_foods = all_foods[1:] #Removing the -- from the first index
    #print(all_foods)
    split_foods = splitAllFoods(all_foods)
    #print(split_foods)

    for i in range(len(split_foods)):
        for j in range(1,len(split_foods[i])):
            link = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.LINK_TEXT, split_foods[i][j]))
            link.click()
            singleNutritionFact()
            driver.back()

if __name__ == '__main__':
    moveToNutritionPage()
    # print(driver.current_url)
    getNutritionFacts()
    #singleNutritionFact()
    time.sleep(1)
    driver.quit()
