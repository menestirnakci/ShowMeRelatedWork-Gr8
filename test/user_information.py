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


class UserInformationTest(unittest.TestCase):
    def test_add_update_delete_user_info(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/sign_up")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys(name)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys(surname)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[8]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[10]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[3]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[5]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[6]/button").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[4]/ul/li[1]/a").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/button").click()
        driver.find_element_by_xpath("//*[@id='subject']").send_keys("Hi my name is ", name, ".",
                                                                     "Thank you checking my profile.")
        driver.find_element_by_xpath("//*[@id='city']").send_keys("Istanbul")
        email = username + "@mail.com"
        driver.find_element_by_xpath("//*[@id='email']").send_keys(email)
        driver.find_element_by_xpath("//*[@id='uni']").send_keys("Istanbul Technical University")
        driver.find_element_by_xpath("//*[@id='tel']").send_keys("+90 555 555 55 55")
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/div/div[3]/div/button").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/button[1]").click()
        driver.find_element_by_xpath("//*[@id='subject']").clear()
        driver.find_element_by_xpath("//*[@id='subject']").send_keys("UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE")
        driver.find_element_by_xpath("//*[@id='city']").clear()
        driver.find_element_by_xpath("//*[@id='city']").send_keys("Istanbul UPDATE")
        email = "UPDATE" + email
        driver.find_element_by_xpath("//*[@id='email']").clear()
        driver.find_element_by_xpath("//*[@id='email']").send_keys(email)
        driver.find_element_by_xpath("//*[@id='uni']").clear()
        driver.find_element_by_xpath("//*[@id='uni']").send_keys("UPDATE Technical University")
        driver.find_element_by_xpath("//*[@id='tel']").clear()
        driver.find_element_by_xpath("//*[@id='tel']").send_keys("+90 111 111 11 11")
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/div[2]/div/button").click()
        driver.find_element_by_xpath("//*[@id='home']/form/div/div/button[2]").click()
        print("User Info Add -> Update -> Delete test is successfully completed!")
        time.sleep(2)
        driver.quit()


