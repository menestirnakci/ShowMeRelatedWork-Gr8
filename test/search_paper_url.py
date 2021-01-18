import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SearchKeywordTest(unittest.TestCase):
    def test_search_url_failure(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/dashboard")
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='url']/div/form[1]/input").send_keys("https://www.resealedsfctual.com")
        driver.find_element_by_xpath("//*[@id='url']/div/form[1]/div/button/strong").click()
        print("Paper URL Search Failure test is successfully completed!")
        time.sleep(2)
        driver.quit()

    def test_search_url(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/dashboard")
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='url']/div/form[1]/input").send_keys("https://www.researchgate.net/publication/326319011_Intellectual_capital_knowledge_management_and_social_capital_within_the_ICT_sector_in_Jordan")
        driver.find_element_by_xpath("//*[@id='url']/div/form[1]/div/button/strong").click()
        print("Paper URL Search test is successfully completed!")
        time.sleep(2)
        driver.quit()

    def test_search_url_graph_functionalities(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/dashboard")
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='url']/div/form[1]/input").send_keys("https://www.researchgate.net/publication/326319011_Intellectual_capital_knowledge_management_and_social_capital_within_the_ICT_sector_in_Jordan")
        driver.find_element_by_xpath("//*[@id='url']/div/form[1]/div/button/strong").click()
        driver.find_element_by_xpath("//*[@id='buttons']/a[2]").click()
        driver.find_element_by_xpath("//*[@id='savebutton']").click()
        driver.find_element_by_xpath("//*[@id='jsonCitations']").click()
        driver.find_element_by_xpath("//*[@id='csvCitations']").click()
        driver.find_element_by_xpath("//*[@id='jsonReferences']").click()
        driver.find_element_by_xpath("//*[@id='csvReferences']").click()
        driver.find_element_by_xpath("//*[@id='jsonPaper']").click()
        driver.find_element_by_xpath("//*[@id='csvPaper']").click()
        driver.find_element_by_xpath("//*[@id='buttons']/a[2]").click()
        driver.find_element_by_xpath("//*[@id='howtowork']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='howtowork1']/div/span").click()
        driver.find_element_by_xpath("//*[@id='item2']").click()
        driver.find_element_by_xpath("//*[@id='iiitem2']/div/form/button[1]/strong").click()
        time.sleep(2)
        driver.find_element_by_xpath("//*[@id='item2']").click()
        driver.find_element_by_xpath("//*[@id='iiitem2']/div/form/button[1]/strong").click()
        print("Graph Functionalities test is successfully completed!")
        time.sleep(2)
        driver.quit()




