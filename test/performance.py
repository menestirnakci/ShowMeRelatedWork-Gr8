import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps, executable_path="chromedriver.exe")

driver.get("http://127.0.0.1:5000/")

logs = [json.loads(log['message'])['message'] for log in driver.get_log('performance')]

with open('devtools.json', 'w') as file:
    json.dump(logs, file)

driver.quit()
