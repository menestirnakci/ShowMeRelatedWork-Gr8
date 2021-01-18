import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import seed
from random import randint
from random_username.generate import generate_username

password = randint(888888888, 8888888888888)
username_list = generate_username(500)
name = ''
surname = ''
for i in username_list:
    if 4 <= len(i) <= 10:
        username = i
        surname = i
        name = i


class BookmarkTest(unittest.TestCase):
    def test_bookmark_add_delete(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/sign_up")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys(name)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys(surname)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[8]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[10]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[3]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[5]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[6]/button").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[4]/ul/li[5]/a").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/button").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/div[1]/div[1]/input").send_keys("https://www.researchgate.net/publication/326319011_Intellectual_capital_knowledge_management_and_social_capital_within_the_ICT_sector_in_Jordan")
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/div[1]/div[2]/input").send_keys("Intellectual capital, knowledge management and social capital within the ICT sector in Jordan")
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/div[2]/div/button").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/table/tbody/tr[2]/td[4]/button/strong").click()
        driver.find_element_by_xpath("//*[@id='item2']").click()
        driver.find_element_by_xpath("//*[@id='iiitem2']/div/form/button[3]/strong").click()
        bookmark_address = "http://127.0.0.1:5000/profile/bookmarks/" + username
        driver.get(bookmark_address)
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/table/tbody/tr[2]/td[4]/button/strong").click()
        driver.find_element_by_xpath("//*[@id='item2']").click()
        driver.find_element_by_xpath("//*[@id='iiitem2']/div/form/button[3]/strong").click()
        bookmark_address = "http://127.0.0.1:5000/profile/bookmarks/"+username
        driver.get(bookmark_address)
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/table/tbody/tr[2]/td[1]/label/input").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/div/div/button").click()
        print("Bookmark Add test is successfully completed!")
        time.sleep(2)
        driver.quit()

