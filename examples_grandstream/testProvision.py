from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webium.controls.link import Link
from webium.driver import get_driver
from webium import BasePage, Find, Finds, Actions
from webium import settings
from webium.plugins import cvs_helper
from webium import wait
import time

wordlist = cvs_helper.load_custom_loc('preset_elm/gs_classic.csv')

class ClassicLoginPage(BasePage):
    login_box = wordlist.return_find_elem('loginbox')
    name_field = wordlist.return_find_elem('usernameinput')
    password_field = wordlist.return_find_elem('passwordinput')
    button = wordlist.return_find_elem('loginsubmit')

class MainPage(BasePage):
    ver_label = Find(by=By.XPATH, value='//*[@id="verNo"]/div')
    reboot_link_btn = Find(by=By.LINK_TEXT, value="Reboot")
    reboot_ok_btn = Find(by=By.XPATH, value="//button[@class='button green']")
    label_list = Finds(by=By.XPATH, value='//div[@class="ant-col ant-form-item-control-wrapper"]/div/span/div/div[@class="ant-row"]/div[1]')

class ClassicMainPage(BasePage):
    topbaner = wordlist.return_find_elem('topBanner')
    popoutwindow = wordlist.return_finds_elem('popupContent')
    resetpassword = wordlist.return_finds_elem('resetpassword')

class MaintenanceUpgradePage(BasePage):
    upgradeNoConfRadio = Find(by=By.XPATH, value='//*[@id="gwt-uid-277"]')
    firmwareServerPath = Find(by=By.XPATH, value='//*[@id="elm-134"]')
    applySaveButton = Find(by=By.XPATH, value='//*[@id="elm-145"]')

class ClassicToolsPage(BasePage):
    provisionButton = Find(by=By.XPATH, value='//*[@id="elm-155"]')

def find_coredump( elem_list ):
    for name in elem_list:
        if name.get_attribute('innerHTML').find('core') != -1:
            return True
    return False

if __name__ == "__main__":
    url = 'http://192.168.92.30'
    home_page = ClassicLoginPage(url=url)
    home_page.open()
    home_page.name_field.send_keys('admin')
    home_page.password_field.send_keys('123456')
    home_page.button.click()
    #
    temp_page = ClassicMainPage(url=url)
    temp_page.open()
    try:
        wait.webiumWait().until(lambda browser: temp_page.popoutwindow)
        if get_driver().find_element_by_xpath('//div[@class="heading"]/div[@class="gwt-HTML"]').get_attribute('textContent') == "Admin Password":
            try:
                i = 0
                for passinputbox in get_driver().find_elements_by_xpath('//input[@class="gwt-PasswordTextBox"]'):
                # for passinputbox in wordlist.return_finds_elem('resetpassword'):
                    try:
                        if i == 0:
                            Actions().move_n_click(passinputbox)
                            passinputbox.send_keys("admin")
                        else:
                            Actions().move_n_click(passinputbox)
                            passinputbox.send_keys("123456")
                    except BaseException as e:
                        print("reset " + repr(e))
                        pass
                    finally:
                        i = i + 1
            except BaseException as e:
                print(repr(e))
            try:
                button_list = get_driver().find_elements_by_class_name("gwt-Button")
                for btn in button_list:
                    if btn.get_attribute("innerHTML") == "Save" and btn.is_displayed():
                        Actions().move_n_click(btn)
            except BaseException as e:
                print("Click save password " + repr(e))
    except TimeoutException:
        pass