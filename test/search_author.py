import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SearchKeywordTest(unittest.TestCase):
    def test_search_author(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/dashboard")
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='warningAuthors']/button").click()
        driver.find_element_by_xpath("//*[@id='Demo']/a[4]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='author']/div/form[1]/input").send_keys("Samer Eid Dahiyat")
        driver.find_element_by_xpath("//*[@id='author']/div/form[1]/div/button/strong").click()
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/table/tbody/tr[1]/td/button").click()
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/table/tbody/tr[1]/td/button").click()
        print("Author Search test is successfully completed!")
        time.sleep(2)
        driver.quit()




