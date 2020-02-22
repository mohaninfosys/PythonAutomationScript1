import sys
import time
import config
import drivers
import screenshot
import requests
import os
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from commonMethods.jsonLoader import jsonLoader
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

data = []
config_file = config.config_path
configObj = jsonLoader.json_read(config_file)

chrome_driver = drivers.chrome_path
firefox_driver = drivers.firefox_path
ie_driver = drivers.ie_path

screenshot_file = screenshot.screenshot_dir_path
folder_name = time.strftime('%d-%m-%Y %H-%M-%S')
os.makedirs(screenshot_file + '/' + folder_name)


class commonUtils(object):

    def __init__(self):
        self.configObj = configObj

    @staticmethod
    def setdriver(drivertype):
        global driver
        options = Options()
        options.add_argument(configObj["driver_config"]["firefox"])
        if drivertype == "chrome":
            # options = webdriver.ChromeOptions()
            # options.add_argument(configObj["driver_config"]["chrome"])
            # options.add_argument("--window-size=1920x1080")
            driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver)
            data.append({"Browser": "Chrome"})
        elif drivertype == "firefox":
            driver = webdriver.Firefox(firefox_options=options, executable_path=firefox_driver)
            data.append({"Browser": "Firefox"})
        elif drivertype == "IE":
            caps = DesiredCapabilities.INTERNETEXPLORER
            caps['ignoreProtectedModeSettings'] = True
            driver = webdriver.Ie(capabilities=caps, executable_path=ie_driver)
        else:
            driver = webdriver.Chrome(executable_path=chrome_driver)

    def logixurl(self):
        commonUtils.get(configObj["logix"]["url"])

    def getdriver(self):
        return driver

    @staticmethod
    def get(url):
        # time.sleep(3)
        driver.maximize_window()
        driver.get(url)
        data.append({"method": "GET - URL Launched", "Action": url})

    @staticmethod
    def write_Json():

        jsonLoader.json_write(data)

    @staticmethod
    def opennewtab(url):
        try:
            time.sleep(2)
            driver.switch_to_window(driver.window_handle[1])
        except:
            driver.execute_script("window.open('" + url + "','new window')")
            driver.switch_to_window("new window")


    @staticmethod
    def closenewtab():
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

    @staticmethod
    def closedriver(self):
        driver.close()

    @staticmethod
    def waitforlocator(xpath):
       try:
           first_result = ui.WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath(xpath))
           we = driver.find_element_by_xpath(xpath)
           return we
       except TimeoutException:
           print("Element Not found")
           if sys.exc_info()[0]:
               print("123")
               commonUtils.takescreenshot()

    @staticmethod
    def exception():
        commonUtils.takescreenshot()
        commonUtils.teardown()

    @staticmethod
    def click(xpath):
        webelement = commonUtils.waitforlocator(xpath)
        try:
            if webelement.is_displayed():
                webelement.click()
                data.append({"method": "Clicked on", "Action": xpath})
            else:
                return False
        except Exception as e:
            if sys.exc_info()[0]:
                commonUtils.takescreenshot()
            print(e)

    @staticmethod
    def takescreenshot():
        driver.get_screenshot_as_file(
            screenshot_file + '/' + folder_name + '/' + (time.strftime('%d %H-%M-%S')) + ".png")

    @staticmethod
    def enterkeys(xpath, keystosend):
        webelement = commonUtils.waitforlocator(xpath)
        try:
            webelement.send_keys(keystosend)
            data.append({"method": "Keys Entered", "Action": keystosend})
        except Exception as e:
            print
            e

    @staticmethod
    def teardown():
        if sys.exc_info()[0]:
            commonUtils.takescreenshot()
        driver.quit()

    @staticmethod
    def gettext(xpath):
        webelement = commonUtils.waitforlocator(xpath)
        try:
            text = webelement.text
            commonUtils.takescreenshot()
            return text
        except Exception as e:
            commonUtils.exception()
            print
            e

    @staticmethod
    def getinnertext(xpath):
        webelem = driver.find_element_by_xpath(xpath)
        return webelem.get_attribute('textContent')

    @staticmethod
    def highlight(element):
        driver = element._parent

        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
            original_style = element.get_attribute('style')
            apply_style("background: yellow; border: 2px solid red;")
            time.sleep(.3)
            apply_style(original_style)

    @staticmethod
    def getattribute(xpath, locatorname):
        webelement = commonUtils.waitforlocator(xpath)
        return webelement.get_attribute(locatorname)

    @staticmethod
    def isdisplayed(xpath):
        try:
            webelement = driver.find_element_by_xpath(xpath)
            return webelement.is_displayed()
        except:
            return False

    @staticmethod
    def isselected(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        return webelement.is_selected()

    @staticmethod
    def isvisible(xpath):
        mwait = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(By.XPATH, xpath))
        return mwait

    @staticmethod
    def isenabled(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        return webelement.is_enabled()

    @staticmethod
    def findelements(xpath):
        listdummy = []
        try:
            webelement = driver.find_elements_by_xpath(xpath)
            count = webelement.size()

            for i in range(count):
                temp = webelement.get(i).text()
                listdummy = listdummy.append(temp)

        except Exception as e:
            assert False
        return listdummy

    @staticmethod
    def actionclick(xpath):
        webelement = commonUtils.waitforlocator(xpath)
        try:
            time.sleep(.1)
            if webelement.is_enabled():
                action = ActionChains(driver)
                action.click(webelement).perform()
            else:
                assert False
        except Exception as e:

            assert False

    @staticmethod
    def actiontype(xpath, keystosend):
        webelement = driver.find_element_by_xpath(xpath)
        try:

            if webelement.is_enabled():
                action = ActionChains(driver)
                action.send_keys(xpath, keystosend).perform()
            else:
                assert False
        except Exception as e:

            assert False

    @staticmethod
    def doubleclick(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        action = ActionChains(driver).double_click(webelement)
        action.perform()

    @staticmethod
    def clear(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        webelement.clear()

    @staticmethod
    def clearandtype(xpath, keystosend):
        try:
            webelement = driver.find_element_by_xpath(xpath)
            webelement.clear()
            webelement.send_keys(keystosend)
        except Exception as e:
            assert False

    @staticmethod
    def mouseover(xpath):
        try:
            webelement = commonUtils.waitforlocator(xpath)
            action = ActionChains(driver)
            action.move_to_element(webelement).perform()
        except Exception as e:
            assert False

    @staticmethod
    def mouseoverandclick(xpath):
        webelement = commonUtils.waitforlocator(xpath)
        try:
            action = ActionChains(driver)
            action.move_to_element(webelement).click().perform()
        except Exception as e:
            assert False

    @staticmethod
    def selectbyvisibletext(xpath, inputdata):
        try:
            select = Select(driver.find_element_by_xpath(xpath))
            select.select_by_visible_text(inputdata)
        except:
            assert False

    @staticmethod
    def selectbyindex(xpath, inputdata):
        webelement = driver.find_element_by_xpath(xpath)
        try:
            if not webelement.is_enabled():
                time.sleep(.2)
                select = Select(webelement)
                select.select_by_index(inputdata)
        except:
            assert False

    @staticmethod
    def selectbyvalue(xpath, text):
        print(xpath, text)
        webelement = driver.find_element_by_xpath(xpath)
        try:
            print("print")
            select = Select(driver.find_element_by_xpath(xpath))
            select.select_by_value(text)
        except Exception as e:
            print(e)

    @staticmethod
    def deselectbyvalue(xpath, value):
        webelement = driver.find_element_by_xpath(xpath)
        try:
            select = Select(webelement)
            select.deselect_by_value(value)
        except:
            assert False

    @staticmethod
    def deselectbyindex(xpath, index):
        webelement = driver.find_element_by_xpath(xpath)
        try:
            select = Select(webelement)
            select.deselect_by_index(index)
        except:
            assert False

    @staticmethod
    def clickandhold(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        action = ActionChains(driver)
        action.click_and_hold(webelement).perform()

    @staticmethod
    def getcurrenturl():
        try:
            return driver.current_url
        except Exception as e:
            return False

    @staticmethod
    def selectcheckbox(xpath):
        webelement = commonUtils.waitforlocator(xpath)
        if webelement is not None:
            if webelement.is_selected():
                return True
            else:
                webelement.click()
        else:
            return False

    @staticmethod
    def deselectcheckbox(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        if webelement.is_selected():
            webelement.click()
        else:
            return False

    @staticmethod
    def switchtab(self):
        driver.switch_to.window(driver.window_handles[1])

    @staticmethod
    def switchtab2(self):
        driver.switch_to.window(driver.window_handles[2])

    @staticmethod
    def switchwindow(self):
        driver.switch_to.window(driver.window_handles(0))

    @staticmethod
    def switchdefaultcontent(self):
        driver.switch_to.default_content()

    @staticmethod
    def draganddrop(dragxpath, dropxpath):
        webelement = driver.find_element_by_xpath(dragxpath)
        webelement1 = driver.find_element_by_xpath(dropxpath)
        action = ActionChains(driver)
        action.drag_and_drop(webelement, webelement1).perform()

    @staticmethod
    def elementisselected(xpath):
        try:
            webelement = driver.find_element_by_xpath(xpath)
            webelement.is_selected()
        except:
            return False

    @staticmethod
    def verifyelementispresent(xpath):
        try:
            webelement = driver.find_element_by_xpath(xpath)
            # commonUtils.highlight(xpath)
            webelement.is_displayed()
            return True
        except:
            return False

    @staticmethod
    def verifyelementisnotpresent(xpath):
        webelement = driver.find_element_by_xpath()
        mwait = WebDriverWait(driver, 5)

    @staticmethod
    def tab(self):
        action = ActionChains(driver)
        action.send_keys(Keys.TAB).perform()

    @staticmethod
    def randomnumber():
        return (time.strftime('%d%H%M%S'))

    @staticmethod
    def getlogixotp():
        commonUtils.opennewtab(configObj["phpmyadmin"]["url"])
        commonUtils.enterkeys("//input[@id='input_username']", configObj["phpmyadmin"]["user"]);
        commonUtils.enterkeys("//input[@id='input_password']", configObj["phpmyadmin"]["password"]);
        commonUtils.click("//input[@value='Go']");
        userid = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[1]")
        if userid == "25":
            loginotp = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[6])[1]")
        else:
            for i in range(2, 20):
                userid = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[" + i + "]")
                if userid is 25:
                    loginotp = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[" + i + "]")
                    break
        commonUtils.closenewtab()
        return loginotp

    @staticmethod
    def getcustomerotp():
        commonUtils.opennewtab(configObj["phpmyadmin"]["customerotpURL"])
        if(commonUtils.isdisplayed("//input[@id='input_username']")):
            commonUtils.enterkeys("//input[@id='input_username']", configObj["phpmyadmin"]["user"])
            commonUtils.enterkeys("//input[@id='input_password']", configObj["phpmyadmin"]["password"])
            commonUtils.click("//input[@value='Go']")
        commonUtils.refreshpage()
        userid = commonUtils.gettext("//table[@id='table_results']/tbody/tr/td[7]")
        if userid == "+91-9600466162":
            loginotp = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[8])[1]")
        else:
            for i in range(2, 20):
                userid = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[7])[" + i + "]")
                if userid is +91-9600466162:
                    loginotp = commonUtils.gettext("(//table[@id='table_results']/tbody/tr/td[8])[" + i + "]")
                    break
        driver.switch_to_window(driver.window_handles[0])
        return loginotp

    def waitUntilVisibilityOfElement(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        mwait = WebDriverWait(driver, 5)
        mwait.until(EC.visibility_of_element_located((By.Xpath, xpath)))

    def getvalue(xpath):
        webelement = driver.find_element_by_xpath(xpath)
        textInsideInputBox = webelement.get_attribute("value")
        if textInsideInputBox in None:
            return "field is empty"
        else:
            return textInsideInputBox

    def sumOfTwoString(str1, str2):
        sum = str1 + str2
        return sum

    def refreshpage():
        try:
            WebDriverWait(driver, 2)
            driver.refresh()
        except:
            driver.execute_script("location.reload()")

    def goback(self):
        try:
            driver.back()
            driver.refresh()
        except:
            driver.execute_script("window.history.go(-1)")

    def goforward(self):
        driver.forward()

    def enter(xpath, keystosend):
        driver.find_element_by_xpath(xpath).send_keys(keystosend, Keys.ENTER)

    def alertok(self):
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert()
            alert.accept()
        except:
            alert = driver.switch_to_alert()
            alert.accept()

    def alertdismiss(self):
        alert = driver.switch_to.alert()
        alert.dismiss()

    def alerttext(self):
        alert = driver.switch_to.alert()
        return alert.text

    def scrollbottom(self):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scrollup(self):
        self.web_driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

    def scrollmid(self):
        driver.execute_script(self, "window.scrollTo(0,300);")

    def timesleep(self):
        print("tsets")
        time.sleep(5)
        print("{}}{}")

    def switchToFrame(self):
        # try:
        print("login")
        driver.switch_to.frame(1)
        print("test")
        driver.switchTo().defaultContent();
        driver.find_element_by_xpath("(//*[@id='announcement_form']//iframe")
        driver.switchTo().activeElement().sendKeys("Hello!")
        print("pass")
        # commonUtils.enterkeys(x)

    # except:
    #     print("It's not: ", x)

    def postapi(details, url):
        try:
            ali_response = requests.post(url=url, data=details)
            if ali_response.status_code == 200:
                return ali_response.json()
            else:
                return False
        except:
            print(str(ali_response.status_code) + "-> api is not working")

    def getapi(details, url):
        try:
            ali_response = requests.get(url=url)
            if ali_response.status_code == 200:
                return ali_response.json()
            else:
                return False
        except:
            print(str(ali_response.status_code) + "-> api is not working")
