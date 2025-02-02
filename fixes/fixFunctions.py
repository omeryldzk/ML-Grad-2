
from selenium.common import NoSuchElementException

from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def determineRegion(regionFile,regionCsv,cityName):
    regionFile.seek(0)
    region = ""
    for row in regionCsv:
        if cityName == row[1]:
            return row[2]
    return region



def closePopUp(driver,wait):
    try:
        close_button = driver.find_elements(By.XPATH,
                                                 """//span[@class="featherlight-close-icon featherlight-close"]""")
    except NoSuchElementException:
        pass
    else:
        if len(close_button) == 1:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")))
            driver.execute_script('arguments[0].click()', close_button[0])
            actions = ActionChains(driver)
            actions.move_by_offset(0, 0).click().perform()
        elif len(close_button) > 1:
            driver.execute_script('arguments[0].click()', close_button[1])
            try:
                close_button = driver.find_elements(By.XPATH,
                                                         """//span[@class="featherlight-close-icon featherlight-close"]""")
            except NoSuchElementException:
                pass
            else:
                close_button2 = driver.find_element(By.XPATH,
                                                         """//span[@class="featherlight-close-icon featherlight-close"]""")
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")))
                driver.execute_script('arguments[0].click()', close_button2)
                actions = ActionChains(driver)
                actions.move_by_offset(0, 0).click().perform()
        else:
            pass
    return
def openAll(driver,wait):
    wait.until(EC.presence_of_element_located((By.XPATH, """//a[@class="label label-success openall"]""")))
    wait.until(EC.element_to_be_clickable((By.XPATH, """//a[@class="label label-success openall"]""")))
    open_all_button = driver.find_element(By.XPATH, """//a[@class="label label-success openall"]""")
    driver.execute_script('arguments[0].click()', open_all_button)
    return 

def clickYear(driver, wait, year):
    wait.until(EC.presence_of_element_located((By.XPATH, """//div[@class="panel panel-default"]""")))
    temp = driver.find_element(By.XPATH, """//div[@class="panel panel-default"]""")
    try:
        yearButton = temp.find_element(By.XPATH, ".//font[text()=\"" + str(year) + " Yılı\"]")
    except NoSuchElementException:
        return 1
    else:
        wait.until(EC.element_to_be_clickable((By.XPATH, ".//font[text()=\"" + str(year) + " Yılı\"]")))
        yearButton = yearButton.find_element(By.XPATH, "./..")
        driver.execute_script('arguments[0].click()', yearButton)
    return 0