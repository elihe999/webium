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
    label_list = Finds(by=By.XPATH, value='//*[@class="data-list"]/tbody/tr/td/div/table/tbody/tr[@class="table-row"]/td[1]//div[@class="gwt-HTML last"]')
    ver_label = Find(by=By.XPATH, value='//*[@id="verNo"]/div')
    reboot_link_btn = Find(by=By.LINK_TEXT, value="Reboot")
    reboot_ok_btn = Find(by=By.XPATH, value="//button[@class='button green']")
    
def find_coredump(label_list):
    get_driver().implicitly_wait(5)
    flag = 1
    count_core = 0
    for item in label_list:
        if item.get_attribute("textContent").find("core") != -1:
            flag = 0
            count_core = count_core + 1
    if flag == 1:
        return 0


if __name__ == '__main__':
    url = 'http://192.168.92.32'

    home_page = ClassicLoginPage(url=url)
    home_page.open()
    home_page.name_field.send_keys('admin')
    home_page.password_field.send_keys('123456')
    home_page.button.click()
    #page:status_system_info
    main_page = MainPage(url=url+"#page:status_system_info")
    main_page.open()
    time.sleep(5)
    print(main_page.ver_label.get_attribute('textContent'))
    find_coredump(main_page.label_list)
    time.sleep(1)
    main_page.reboot_link_btn.click()
    wait.webiumWait().until(lambda browser: main_page.reboot_ok_btn)
    main_page.reboot_ok_btn.click()
    get_driver().quit()
