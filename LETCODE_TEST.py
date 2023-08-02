import time

from faker import Faker
from random import randint

import unittest

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import color
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert

fake = Faker()


class Letcode_test(unittest.TestCase):

    def setUp(self):
        opts = webdriver.FirefoxOptions()
        opts.add_argument('--start-maximized')
        opts.add_argument('--disable-extensions')
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.maximize_window()


    def test_Input_Field(self):
        driver = self.driver
        driver.get("https://letcode.in/test")
        driver.find_element(By.CLASS_NAME, "card-footer-item").click() # click edit button
        driver.find_element(By.ID, "fullName").send_keys(fake.name())
        tab_keys = driver.find_element(By.ID, "join")
        tab_keys.send_keys(fake.text())
        tab_keys.send_keys(Keys.TAB)
        time.sleep(3)

        #what is inside the placholder
        inside_text_box = driver.find_element(By.ID, "getMe")
        val = inside_text_box.get_attribute("value")
        print(" Inside the text box is" + " " + val)

        # clear the text
        driver.find_element(By.ID, "clearMe").clear()

        # Confirm edit field is disabled
        test_enabled = driver.find_element(By.ID, "noEdit").is_enabled()
        if str(test_enabled) == "False":
            print("All good edit field is disabled")
        else:
            print("Not OK edit field is enable")

        #Confirm text is readonly
        read_only = driver.find_element(By.ID, "dontwrite").get_attribute("value")
        if read_only == "This text is readonly":
            print("ALL GOOD the element is read-only")
        else:
            print("the element is NOT read-only")
    def test_Button_field(self):
        driver = self.driver
        driver.get("https://letcode.in/buttons")
        time.sleep(3)

        #Goto Home and come back here using driver command
        driver.find_element(By.ID, "home").click()
        driver.back()

        #Get the X & Y co-ordinates
        location = driver.find_element(By.ID, "position").location
        print("X & Y co-ordinates is " + " " + str(location))

        #Find the color of the button
        colorr = driver.find_element(By.ID, "color").value_of_css_property('background-color')
        print("The color of the button is" + " " + colorr)

        #Find the height & width of the button
        button = driver.find_element(By.ID, "property")
        button_height = button.size['height']
        button_width = button.size['width']
        print("Button Height:", button_height, "px")
        print("Button Width:", button_width, "px")

        #Confirm button is disabled
        test_enabled = driver.find_element(By.XPATH, "//button[contains(text(),'Disabled')]").is_enabled()
        if str(test_enabled) == "False":
            print("All good edit field is disabled")
        else:
            print("Not OK edit field is enable")

        #Click and Hold Button
        element = driver.find_element(By.XPATH, "//button[contains(.,'Button has been long pressed')]")
        action = ActionChains(driver)
        click = ActionChains(driver)
        action.click_and_hold(element)
        action.perform()
        time.sleep(10)
        action.release(element)
        action.perform()
        time.sleep(0.2)
        action.release(element)






    def tearDown(self):
        self.driver.quit()


