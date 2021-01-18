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


class UserTest(unittest.TestCase):
    def test_delete_account(self):
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
        driver.find_element_by_xpath("/html/body/div[3]/div[4]/ul/li[6]/a").click()
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/form/div/input").send_keys("asdasdasd")
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/form/button").click()
        time.sleep(2)
        delete_account_page = "http://127.0.0.1:5000/profile/delete_account/" + username
        driver.get(delete_account_page)
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/form/div/input").send_keys(password)
        driver.find_element_by_xpath("//*[@id='home']/div[2]/div/div/div/form/button").click()
        print("Delete Account Fail and Success test is successfully completed!")
        time.sleep(3)
        driver.quit()

    def test_sign_up(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/sign_up")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys(name)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys(surname)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[8]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[10]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        print("Sign up test is successfully completed!")
        time.sleep(2)
        driver.quit()

    def test_sign_up_username_taken(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/sign_up")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys(surname)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[8]/input").send_keys("enes")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[10]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        print("Sign up username has already taken failure test is successfully completed!")
        time.sleep(2)
        driver.quit()

    def test_follow_unfollow(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/login")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys("enes")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys("1111111111111111")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[5]/button").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[4]/ul/li[2]/a").click()
        driver.find_element_by_xpath("/html/body/div/div/div/div[16]/div/div[2]/form/button/strong").click()
        driver.find_element_by_xpath("/html/body/nav/div/div/div/span[2]/a").click()
        driver.find_element_by_xpath("/html/body/div[3]/div[4]/ul/li[3]/a").click()
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[2]/form/button/strong").click()
        print("Follow/Unfollow test is successfully completed!")
        time.sleep(2)
        driver.quit()

    def test_sign_up_length(self):
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("http://127.0.0.1:5000/sign_up")
        driver.maximize_window()
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys("a")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys("b")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[8]/input").send_keys("ab")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[10]/input").send_keys("112")
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[2]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[4]/input").send_keys(surname)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[8]/input").send_keys(username)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[10]/input").send_keys(password)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/form/div[11]/button").click()
        print("Sign up required text areas minimum length test is successfully completed!")
        time.sleep(2)
        driver.quit()


