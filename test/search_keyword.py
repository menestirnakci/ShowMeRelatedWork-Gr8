import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SearchKeywordTest(unittest.TestCase):
    def test_search_keyword(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/dashboard")
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='warningAuthors']/button").click()
        driver.find_element_by_xpath("//*[@id='Demo']/a[3]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='keyword']/div/form[1]/input").send_keys("ai")
        driver.find_element_by_xpath("//*[@id='keyword']/div/form[1]/div/button/strong").click()
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/table/tbody/tr[1]/td/button").click()
        print("Keyword Search test is successfully completed!")
        time.sleep(2)
        driver.quit()



