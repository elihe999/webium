from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webium.controls.link import Link
from webium.controls.select import Select

from webium.driver import get_driver
from webium import BasePage, Find, Finds, Actions
from webium import settings
from webium.plugins import cvs_helper
from webium import wait
import time

wordListClassic = cvs_helper.load_custom_loc('preset_elm/gs_classic.csv')
wordListAntD = cvs_helper.load_custom_loc('preset_elm/gs_antd.csv')

class AntDesignLoginPage(BasePage):
    login_box = wordListAntD.return_find_elem('loginbox')
    name_field = wordListAntD.return_find_elem('usernameinput')
    password_field = wordListAntD.return_find_elem('passwordinput')
    button = wordListAntD.return_find_elem('loginsubmit')
    # language
    lang_select = wordListAntD.return_find_elem('loginboxlangselect')

class AntDesignMainPage(BasePage):
    pass

class ClassicLoginPage(BasePage):
    login_box = wordListClassic.return_find_elem('loginbox')
    name_field = wordListClassic.return_find_elem('usernameinput')
    password_field = wordListClassic.return_find_elem('passwordinput')
    button = wordListClassic.return_find_elem('loginsubmit')
    # language
    lang_select = wordListClassic.return_simple_string('loginboxlangselect')
    lang_select_box = Find(Select, By.XPATH, lang_select)

class ClassicMainPage(BasePage):
    reboot_link_btn = Find(by=By.LINK_TEXT, value="Reboot")
    ver_label = Find(by=By.XPATH, value='//*[@id="verNo"]/div')
    reboot_ok_btn = Find(by=By.XPATH, value="//button[@class='button green']")
    label_list = Finds(by=By.XPATH, value='//div[@class="ant-col ant-form-item-control-wrapper"]/div/span/div/div[@class="ant-row"]/div[1]')
    topbaner = wordListClassic.return_find_elem('topBanner')
    popoutwindow = wordListClassic.return_finds_elem('popupContent')
    resetpassword = wordListClassic.return_finds_elem('resetpassword')

class AccountInfo():
    username = ''
    password = ''
    loop = 1
    interval = 100

def change_language(ui_style, page):
    if ui_style == "classic":
        page.lang_select_box.select_option('English')
    elif ui_style == "antd":
        Actions().move_n_click(page.lang_select)
    else:
        raise IndexError("Not matching UI")

def find_coredump(elem_list):
    for name in elem_list:
        if name.get_attribute('innerHTML').find('core') != -1:
            return True
    return False

def reboot(aurl, username, password, style):
    tester = AccountInfo()
    url = aurl
    tester.username = username
    tester.password = password
    home_page = ClassicLoginPage(url=url)
    home_page.open()
    # change language
    change_language(style, home_page)
    home_page.name_field.send_keys(tester.username)
    home_page.password_field.send_keys(tester.password)
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
                    try:
                        if i == 0:
                            Actions().move_n_click(passinputbox)
                            passinputbox.send_keys(tester.username)
                        else:
                            Actions().move_n_click(passinputbox)
                            passinputbox.send_keys(tester.password)
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
    main_page = ClassicMainPage(url=url+"#page:status_system_info")
    main_page.open()
    time.sleep(5)
    main_page.refresh
    label_list = Finds(by=By.XPATH, value='//*[@class="data-list"]/tbody/tr/td/div/table/tbody/tr[@class="table-row"]/td[1]//div[@class="gwt-HTML last"]')
    print(main_page.ver_label.get_attribute('textContent'))
    time.sleep(1)
    main_page.reboot_link_btn.click()
    wait.webiumWait().until(lambda browser: main_page.reboot_ok_btn)
    main_page.reboot_ok_btn.click()
    get_driver().quit()

if __name__ == "__main__":
    url = 'http://192.168.92.57'
    username = 'admin'
    password = '123456'
    style = "classic"
    reboot(url, username, password, style)