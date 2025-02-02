import csv
from selenium import webdriver
import platform

from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fixFunctions import *


file = open("fulldata_clean(fixed).csv", "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

helperFile = open("sudden_changes_single_row_2times.csv", "r", encoding="utf-8")
csvreaderHelper = csv.reader(helperFile)

fixedFileName = "fulldata_clean(fixed).csv".replace(".csv", "") + "(fixed)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)


if platform.system() == "Darwin":
    path = '../resources/mac_chrome_driver/chromedriver'
elif platform.system() == "Windows":
    path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
    
cService = webdriver.ChromeService(executable_path=path)
driver = webdriver.Chrome(service=cService)
wait = WebDriverWait(driver, 30)

helperDict = {}

for row in csvreaderHelper:
    helperDict[(str(row[0]).replace(".0",""), str(row[5]).replace(".0",""))] = row


# Write the header
try:
    header = next(csvreaderFileToFix)
    csvwriter.writerow(header)
except StopIteration:
    print("The input CSV file is empty.")
    file.close()
    helperFile.close()
    newFile.close()
    exit()


for row in csvreaderFileToFix:
    if (str(row[0]).replace(".0",""), str(row[5]).replace(".0","")) in helperDict and row[0] != "2021":
        idOsym = str(row[5]).replace(".0", "")
        academicYear = str(row[0]).replace(".0", "")
        link = "https://yokatlas.yok.gov.tr/lisans.php?y=" + idOsym
        driver.get(link)
        
        # Check if the URL is one of the "anasayfa" URLs
        if driver.current_url in [
            "https://yokatlas.yok.gov.tr/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2023/lisans-anasayfa.php"
        ]:
            csvwriter.writerow(row)
            newFile.flush()
            continue
        
        # Check if the body contains "File not found."
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "File not found." in body_text:
            csvwriter.writerow(row)
            newFile.flush()
            continue
        
        closePopUp(driver, wait)
        
        # Check again if the URL is one of the "anasayfa" URLs after closing the popup
        if driver.current_url in [
            "https://yokatlas.yok.gov.tr/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2023/lisans-anasayfa.php"
        ]:
            csvwriter.writerow(row)
            newFile.flush()
            continue
        
        if clickYear(driver, wait, academicYear) == 1:
            csvwriter.writerow(row)
            newFile.flush()
            continue
        
        # Check again if the URL is one of the "anasayfa" URLs after clicking the year
        if driver.current_url in [
            "https://yokatlas.yok.gov.tr/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php",
            "https://yokatlas.yok.gov.tr/2023/lisans-anasayfa.php"
        ]:
            csvwriter.writerow(row)
            newFile.flush()
            continue
        
        openAll(driver, wait)
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1070"]""")))
        lastPersonSection = driver.find_element(By.XPATH, """//div[@id="icerik_1070"]""")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1070 table""")))
        table = lastPersonSection.find_element(By.XPATH, """.//table[@class="table table-bordered"]""")
        rows = table.find_elements(By.XPATH, """.//tr""")
        baseRanking = ""
        for row2 in rows:
            cols = row2.find_elements(By.XPATH, """.//td""")
            if cols[0].text in ["Yerleştiği Başarı Sırası*", "Yerleştiği Başarı Sırası *"]:
                baseRanking = cols[1].text
        baseRanking = baseRanking.replace(".", "")
        row[19] = baseRanking
    
    csvwriter.writerow(row)
    newFile.flush()