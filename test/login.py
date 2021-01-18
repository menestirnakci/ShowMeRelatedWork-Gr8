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


class LoginTest(unittest.TestCase):
    def test_login_log_out(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/login")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys("enes")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys("1111111111111111")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[5]/button").click()  # Sign In button
        driver.find_element_by_xpath("/html/body/div[2]/nav/div/div/span[1]/a").click()  # Log out button
        print("Login and logout process are successfully completed!")
        time.sleep(2)
        driver.quit()

    def test_login_fail(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/login")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys("enes")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys("11111saasd")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[5]/button").click()
        print("Test of failure login process are successfully completed!")
        time.sleep(2)
        driver.quit()


