import time
from unittest import TestCase

from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object)


class WebpageTests(TestCase):

    def test_title(self):
        """Make sure title is correct"""
        driver.get('http://127.0.0.1:8000')
        self.assertEqual(driver.title, "Chat")

    def test_login(self):
        driver.get('http://127.0.0.1:8000/login/')
        driver.find_elements(By.CLASS_NAME, 'form-control')[0].send_keys('Hristijan')
        driver.find_elements(By.CLASS_NAME, 'form-control')[1].send_keys('testing321')
        driver.find_element(By.CLASS_NAME, 'btn').click()

    def test_send_message(self):
        """Test posting message, and number of articles"""
        self.test_login()

        driver.get('http://127.0.0.1:8000')
        time.sleep(1)
        num_messages = len(driver.find_elements(By.CLASS_NAME, 'message'))

        driver.find_element(By.CLASS_NAME, 'form-control').send_keys('Test Test Test Test Test Test Test ')
        driver.find_element(By.ID, 'send-message').click()

        time.sleep(1)
        after_click_num_messages = len(driver.find_elements(By.CLASS_NAME, 'message'))
        self.assertEqual(num_messages + 1, after_click_num_messages)

    def test_add_new_group(self):
        self.test_login()
        driver.get('http://127.0.0.1:8000')

        e = driver.find_element(By.CLASS_NAME, 'btn-success')
        driver.execute_script("arguments[0].click();", e)

        driver.find_elements(By.CLASS_NAME, 'form-control')[0].send_keys('Group name3')
        driver.find_elements(By.CLASS_NAME, 'form-control')[1].send_keys('Desc3')

        # click all users
        for i in driver.find_elements(By.CLASS_NAME, 'ml-5'):
            i.click()

        driver.find_element(By.CLASS_NAME, 'btn').click()

    def test_update_group(self):
        self.test_login()
        driver.get('http://127.0.0.1:8000')

        e = driver.find_element(By.CLASS_NAME, 'update')
        driver.execute_script("arguments[0].click();", e)

        input1 = driver.find_elements(By.CLASS_NAME, 'form-control')[0]
        driver.execute_script("arguments[0].value = arguments[1];", input1,'Frontend2')

        input2 = driver.find_elements(By.CLASS_NAME, 'form-control')[1]
        driver.execute_script("arguments[0].value = arguments[1];", input2,'all about frontend')

        driver.find_element(By.CLASS_NAME, 'btn').click()
