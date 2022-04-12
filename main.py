from selenium import webdriver
# from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
import time
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC


# Setup for web scrap. Path needs to change for chromedriver.exe once uploaded in the cloud.
from selenium.webdriver.support.wait import WebDriverWait

driver_path = "C:\Program Files (x86)\chromedriver.exe"
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# Starting website
driver.get("https://nutrition.sa.ucsc.edu/")


def moveToNutritionPage():
    dining_location = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME,"locations"))
    print(dining_location.text)

    dining_hall_link = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.LINK_TEXT,dining_location.text))
    dining_hall_link.click()

    nutrition_page = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, "shortmenunutritive"))
    nutrition_page_link = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.LINK_TEXT,nutrition_page.text))

    nutrition_page_link.click()

def singleNutritionFact():
    pass

# Must call moveToNutritionPage() before calling this function.
# Driver current_url should be similar to:
# https://nutrition.sa.ucsc.edu/longmenu.aspx?sName=UC+Santa+Cruz+Dining&locationNum=40&locationName=College+Nine%2fJohn+R.+Lewis+Dining+Hall&naFlag=1&WeeksMenus=UCSC+-+This+Week%27s+Menus&dtdate=04%2f08%2f2022&mealName=Breakfast
def getNutritionFacts():
    get_all_tables = driver.find_elements(By.TAG_NAME, "table")


    # No good way to get food table. Iterate through all tables and get the html code for the 4th table
    size = 0
    whole_page = None
    for i in get_all_tables:
        size += 1
        if size == 4:
            # Getting html for most inner table. Ignore rest
            whole_page = i
            #print(whole_page.get_attribute("innerHTML"))
            break


    food_table = whole_page.find_elements(By.TAG_NAME,"table")

    size = len(food_table) - 1
    # for i in range(0,size,2):
    #     getElement = None
    #     try:
    #         getElement = food_table[i].find_element(By.CLASS_NAME, "longmenucolmenucat")
    #     except:
    #         getElement = food_table[i].find_element(By.CLASS_NAME, "longmenucoldispname")
    #         link = getElement.find_element(By.LINK_TEXT,getElement.text)
    #         link.click()
    #         driver.back()
    #     print(getElement.text)

    getElement = food_table[2].find_element(By.CLASS_NAME, "longmenucoldispname")
    link = getElement.find_element(By.LINK_TEXT, getElement.text)
    link.click()
    driver.back()
    print(size)
    print(len(food_table))
    driver.implicitly_wait(0.5)
    test2 = food_table[4].find_element(By.CLASS_NAME,"longmenucoldispname")

    #print("test: " + test.text)
    # test2 = test.find_element(By.TAG_NAME,"tbody")
    # print("test2: " + test2.text)



if __name__ == '__main__':
    moveToNutritionPage()
    test2 = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.XPATH, '//table[@width="70%"]'))
    print(test2.get_attribute("innerHTML"))

    #print(driver.current_url)
    #getNutritionFacts()
    time.sleep(1)
    driver.quit()
