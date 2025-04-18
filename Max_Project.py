
import time

from faker import Faker
from random import randint

import unittest

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.service import Service as GeckoDriverManager

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert

faker_indent = Faker()


class FirefoxSearch(unittest.TestCase):

    def setUp(self):
        opts = webdriver.FirefoxOptions()
        opts.add_argument('--start-maximized')
        opts.add_argument('--disable-extensions')
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        self.driver.maximize_window()

    def test_amazon_create_login(self):
        driver = self.driver
        driver.get("https://testpages.herokuapp.com/styled/attributes-test.html")
        # elem = driver.find_element(By.ID, "jsattributes")

        for i in range(1, 5):

            elem = driver.find_element(By.ID, "jsattributes")

            if elem.get_attribute('nextid') == str(i):
                print("OK")
            else:
                print("NOT OK nextid different ", i)
            driver.find_element(By.CLASS_NAME, "styled-click-button").click()  # button
            if elem.get_attribute("custom-" + str(i)) == ("value-" + str(i)):
                print("OK value")
            else:
                print("Not OK value is", i)

    def test_Basic_HTML_Form_Example(self):
        driver = self.driver
        driver.get("https://testpages.herokuapp.com/")
        driver.find_element(By.ID, "htmlformtest").click()  # next page HTML Form Example
        check_box_random = randint(0, 2)
        driver.find_elements(By.NAME, "radioval")[randint(0, 2)].click()  # click random radio every time

        driver.find_elements(By.NAME, "checkboxes[]")[check_box_random].click()  # click random checkbox every time
        time.sleep(5)

        Select(driver.find_element(By.NAME, 'dropdown')).select_by_index(
            randint(0, 5))  # choosing random dropdown by Select
        Select(driver.find_element(By.NAME, "multipleselect[]")).select_by_index(
            randint(0, 3))  # Multiple Select Values

        driver.find_elements(By.NAME, "submitbutton")[1].click()
        time.sleep(5)
        # checking if random checkbox have same value with submited form
        submit_form = driver.find_element(By.ID, "_valuecheckboxes0").text

        if "cb" + str(check_box_random + 1) == submit_form:
            print("Form OK")
        else:
            print("Form Bad")

        time.sleep(10)

    def test_Dynamic_HTML_TABLE_Tag(self):
        driver = self.driver

        driver.get("https://testpages.herokuapp.com/")
        driver.find_element(By.ID, "dynamictablestest").click()  # next page Dynamic Table Test Page
        time.sleep(5)
        # checking if title is correct
        try:
            assert driver.title == "Table HTML Tag - JavaScript Created"
            print("Title is Correct. Current Title is:", driver.title)

        except AssertionError:
            print("Title is different. Current Title is:", driver.title)

        # checking if current urs is CORRECT
        acct_reg_expected_url = "https://testpages.herokuapp.com/styled/tag/dynamic-table.html"
        acct_reg_actual_url = driver.current_url
        if acct_reg_expected_url == acct_reg_actual_url:
            print('"Account registration" page URL is correct:', driver.current_url)
        else:
            print('"Account registration" page URL is wrong:', driver.current_url)
        #     #check if header h1 text is correct
        text_website = driver.find_element(By.XPATH, "//h1[contains(.,'Dynamic HTML TABLE Tag')]").text
        text_expected = "Dynamic HTML TABLE Tag"
        if text_website == text_expected:
            try:
                assert text_website == text_expected
                print("Paragraph text is correct. Current text is:", text_website)
            except AssertionError:
                print("Paragraph text is different. Current text is:", text_website)
        driver.find_element(By.TAG_NAME, "p")  # checking first paragraph
        driver.find_element(By.ID, "refreshtable")  # refresh table button
        driver.find_element(By.ID, "caption")  # placeholder Caption
        driver.find_element(By.ID, "tableid")  # placeholder Id

        elems = driver.find_elements(By.TAG_NAME, "a")
        print(type(elems))
        print(elems)

        for elem in elems:

            xpath = driver.execute_script("""
                    var xpath = "";
                    var containerElem = document.documentElement;
                    var elem = arguments[0];

                    while (elem !== containerElem) {
                        var index = 0;
                        var sibling = elem.previousSibling;

                        while (sibling) {
                            if (sibling.nodeType === Node.ELEMENT_NODE && 
                                sibling.nodeName.toLowerCase() === elem.nodeName.toLowerCase()) {
                                index++;
                            }
                            sibling = sibling.previousSibling;
                        }
                        xpath = "/" + elem.nodeName.toLowerCase() + "[" + (index + 1) + "]" + xpath;
                        elem = elem.parentNode;
                    }
                    return "/" + containerElem.nodeName.toLowerCase() + xpath;
            """, elem)  # Checking for correct XPATH
            print("xpath", xpath)
            if elem.get_attribute("hrefd"):
                print("OK for Elements", elem.text)

            else:
                print("NOT OK  for Element", elem.text)

        driver.find_element(By.TAG_NAME, "summary").click()  # Table data
        jsondata = driver.find_element(By.ID, "jsondata")
        jsondata.clear()  # placeholder with json textarea

        data = [{"name": "Bob", "age": 20}, {"name": "George", "age": 42}, {"name": "Max", "age": 20}]

        print(data)

        for i in range(100):
            data.append({"name": faker_indent.first_name(), "age": randint(10, 100)})
            print(data)

        time.sleep(1)

        print(data)
        jsondata.send_keys(str(data).replace("'", '"'))
        time.sleep(4)

        driver.find_element(By.ID, "refreshtable").click()
        time.sleep(10)
        Allelems = driver.find_elements(By.TAG_NAME, "tr")

        if len(Allelems[1:]) == len(data):
            print("lenght is ok")
        else:
            print("lenght is not ok")

        i = 0
        for elem in Allelems[1:]:

            tds = elem.find_elements(By.TAG_NAME, "td")
            if tds[0].text == data[i]["name"] and tds[1].text == str(data[i]["age"]):
                print("OK")
            else:
                print("Not OK", tds[0], "is", data[i]["name"], tds[1], "is", data[i]["age"])
            i += 1

    def test_Alert_Box_Examples(self):
        driver = self.driver
        driver.get("https://testpages.herokuapp.com/")
        driver.find_element(By.ID, "alerttest").click()
        text_website = driver.find_element(By.TAG_NAME, "h1").text
        text_expected = "Alert Box Examples"
        try:
            assert text_website == text_expected
            print("Paragraph text is correct. Current text is:", text_website)
        except AssertionError:
            print("Paragraph text is different. Current text is:", text_website)

        button1 = driver.find_element(By.ID, "alertexamples")  # Button - Show alert box
        button1.click()
        alert = Alert(driver)
        print(alert.text)
        time.sleep(4)
        alert.accept()
        time.sleep(3)
        button2 = driver.find_element(By.ID, "confirmexample")  # Button - Show confirm box
        button3 = driver.find_element(By.ID, "promptexample")  # Button - Show prompt box
        paragraph_website = driver.find_element(By.TAG_NAME, "p").text
        paragraph_expected = "There are three main JavaScript methods which show alert dialogs: alert," \
                             " confirm and prompt. This page has examples of each."

        try:
            assert paragraph_website == paragraph_expected
            print("Paragraph text is correct. Current text is:", paragraph_website)
        except AssertionError:
            print("Paragraph text is different. Current text is:", paragraph_website)

        button2.click()
        alert = Alert(driver)
        print(alert.text)
        time.sleep(4)
        alert.accept()
        if driver.find_element(By.ID, "confirmreturn").text == "true":
            print("OK")
        else:
            print("Not OK")

        time.sleep(3)
        button2.click()
        time.sleep(3)
        alert.dismiss()
        time.sleep(3)

        button3.click()
        time.sleep(3)
        alert.send_keys("Max")
        time.sleep(3)
        alert.accept()
        time.sleep(3)
        if driver.find_element(By.ID, "promptreturn").text == "Max":
            print("OK")
        else:
            print("Not OK")

    def test_Refresh_Page_Test(self):
        driver = self.driver
        driver.get("https://testpages.herokuapp.com/styled/refresh")
        value1 = driver.find_element(By.ID, "embeddedrefreshdatevalue").text
        value2 = driver.find_element(By.ID, "refreshdate").text
        value3 = driver.find_element(By.TAG_NAME, "h1").text.split()[-1]
        driver.refresh()
        time.sleep(2)
        if value3 == value2 == value1:
            print("after Page Refresh the id numbers equal")
        else:
            print("ERROR after Page Refresh the id numbers  is not equal", value3, value1, value2)
        driver.find_element(By.LINK_TEXT, "EvilTester.com").click()
        time.sleep(2)
        driver.close()

    def test_HTML5_Form_Elements_Examples(self):
        driver = self.driver
        driver.get("https://testpages.herokuapp.com/styled/html5-form-test.html")
        # colors = ['128,0,0', '#800000', '#0000FF', '#00FF00', '#FFFF00', '#00FFFF']
        # random_color = random.choice(colors)
        # driver.find_element(By.ID, "colour-picker").send_keys(random_color)
        fake_email = driver.find_element(By.ID, "email-field")
        fake_email.clear()
        fake_email.send_keys(faker_indent.email())
        num = driver.find_element(By.ID, "number-field")
        num.clear()
        num.send_keys(randint(0, 1000))
        data_string = faker_indent.month_name() + " " + faker_indent.year()
        driver.find_element(By.ID, "month-field").send_keys(data_string)
        time.sleep(3)
        # now = datetime.now()
        dt_string = faker_indent.date().split("-")
        dt_string.reverse()
        num_reverse = ("/").join(dt_string)
        num_reverse1 = faker_indent.time()[:-3]
        num_reverse2 = num_reverse + "T" + num_reverse1
        print(num_reverse2)
        # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        clear_data = driver.find_element(By.ID, "date-time-picker")
        clear_data.click()
        clear_data.send_keys(num_reverse2)
        time.sleep(5)
        driver.find_element(By.NAME, "submitbutton").click()
        time.sleep(3)
        submit1 = driver.find_element(By.ID, "_valuedatetime").text
        submit2 = driver.find_element(By.ID, "_valueemail").text
        submit3 = driver.find_element(By.ID, "_valuemonth").text
        submit4 = driver.find_element(By.ID, "_valuenumber").text
        print(type(submit1))
        print(type(dt_string))
        if dt_string == submit1 and submit2 == fake_email:
            print("datetime and email is correct")
        else:
            print("datetime and email is NOT correct")
        if submit3 == data_string and submit4 == num:
            print("month and number is correct")
        else:
            print("month and number is NOT correct")

        time.sleep(3)

    def tearDown(self):
        self.driver.quit()
