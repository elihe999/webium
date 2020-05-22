from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webium.controls.link import Link
from webium.driver import get_driver
from webium import BasePage, Find, Finds, Actions
from webium import settings

class GooglePage(BasePage):
    url = 'http://www.baidu.com'

    text_field = Find(by=By.NAME, value='wd')
    button = Find(by=By.CLASS_NAME, value='soutu-btn')

class ResultItem(WebElement):
    link = Find(Link, By.XPATH, './/h3/a')


class ResultsPage(BasePage):
    stat = Find(by=By.ID, value='resultStats')
    results = Finds(ResultItem, By.XPATH, '//div/li')


if __name__ == '__main__':
    settings.chrome_handless = True
    home_page = GooglePage()
    home_page.open()
    # home_page.text_field.send_keys('Page Object')
    # home_page.button.click()
    Actions().move_n_click(home_page.button)
    # results_page = ResultsPage()
    # print('Results summary: ' + results_page.stat.text)
    # for item in results_page.results:
    #     print(item.link.text)
    # get_driver().quit()
