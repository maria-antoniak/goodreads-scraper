from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chromium.webdriver import ChromiumDriver


def get_web_driver(browser_name: str) -> ChromiumDriver:
    if browser_name == 'chrome':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser_name == 'edge':
        driver = webdriver.Edge()
    else:
        raise ValueError('Please select a web browser: Chrome or Edge')

    return driver
