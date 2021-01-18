import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SearchRecommendedTest(unittest.TestCase):
    def test_recommended_paper(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/dashboard")
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='url']/div/form[2]/button/strong").click()
        print("Recommended Paper test is successfully completed!")
        time.sleep(2)
        driver.quit()



