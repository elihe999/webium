from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver_class = Chrome
implicit_timeout = 30
wait_timeout = 30

chromedriverpath =  r"chromedriver.exe"

default_search_type = By.ID

try:
    from local_webium_settings import *  # noqa
except ImportError:
    pass
