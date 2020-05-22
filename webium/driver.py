import webium.settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
_driver_instance = None


def get_driver():
    chromedriver_path = webium.settings.chromedriverpath
    c_service = Service(chromedriver_path)
    c_service.command_line_args()
    c_service.start()
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-plugins')
    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--disk-cache=yes')
    service_args.append('--ignore-ssl-errors=true')
    global _driver_instance
    if not _driver_instance:
        _driver_instance = webdriver.Chrome(chrome_options=chrome_options, service_args=service_args,
                                            executable_path=chromedriver_path)
        _driver_instance.implicitly_wait(webium.settings.implicit_timeout)
    return _driver_instance


def get_driver_no_init():
    return _driver_instance


def close_driver():
    global _driver_instance
    if _driver_instance:
        _driver_instance.quit()
        _driver_instance = None
