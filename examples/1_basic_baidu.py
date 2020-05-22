from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webium.controls.link import Link
from webium.driver import get_driver
from webium import BasePage, Find, Finds, Actions
from webium import settings
from webium.plugins import cvs_helper

wordlist = cvs_helper.load_custom_loc('preset_elm/my_baidu_example.csv')

class BaiduPage(BasePage):
    url = 'http://www.baidu.com'

    button = wordlist.return_find_elem('searchbtn')
    text_field = wordlist.return_find_elem('searchbar')

class ResultItem(WebElement):
    link = Find(Link, By.XPATH, './/h3/a')


class ResultsPage(BasePage):
    # stat = Find(by=By.ID, value='resultStats')
    results = wordlist.return_finds_elem('firstresult')


if __name__ == '__main__':
    home_page = BaiduPage()
    home_page.open()
    home_page.text_field.send_keys('Page Object')
    # home_page.button.click()
    Actions().move_n_click(home_page.button)
    results_page = ResultsPage()
    # print('Results summary: ' + results_page.stat.text)
    for item in results_page.results:
        # print(item.link.text)
        pass # todo
    get_driver().quit()
    get_driver().quit()
