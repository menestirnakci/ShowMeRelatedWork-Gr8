# pipenv run concurrent
# pipenv run concurrent --num 40
# python stress_test.py
# python stress_test.py --num 100
# pycharm configuration parameter: --num 100 (if you want to add)
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from concurrent.futures import ThreadPoolExecutor, wait
import argparse
import time

t0 = time.time()
parser = argparse.ArgumentParser(description='Stress test the python selenium webdriver')
parser.add_argument('--num', type=int, help='Number of simultaneous instances', default=20)
parser.add_argument('--type', help='How to run the instances', choices=['parallel', 'concurrent'])
args = parser.parse_args()


def run():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    try:
        driver = webdriver.Chrome(
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options,
            executable_path="chromedriver.exe"
        )
        driver.get('http://127.0.0.1:5000')
        driver.close()
        driver.quit()
    except Exception as e:
        raise


num = args.num
with ThreadPoolExecutor(max_workers=num) as executor:
    futures = []
    for _ in range(num):
        futures.append(executor.submit(run))
    wait(futures)
    for f in futures:
        print(f.exception())

t1 = time.time()
total = t1-t0
print("Proccess finished in ", total, " seconds")