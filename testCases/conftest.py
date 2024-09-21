import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from page_objects.home_page import HomePage

# from page_objects.index_page import IndexPage
# from page_objects.login_page import LoginPage


# @pytest.fixture()
# def setup(request):
#     browser = request.config.getoption("--browser")
#
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
#     options.add_argument("start-maximized")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
#     yield driver
#     driver.quit()


import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture()
def setup():
    # Configure Firefox options
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # Set up Firefox driver using GeckoDriverManager
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    # Yield the driver for use in tests
    yield driver

    # Quit the driver after tests are done
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Specify the browser (chrome/firefox/edge)")


@pytest.fixture()
def browser(request):
    return request.config.getoption('--browser')


########################### pytest HTML Report #############################

def pytest_configure(config):
    config._metadata['Project Name'] = 'SoftUni QA'
    config._metadata['Module Name'] = 'CustRegistration'
    config._metadata['Tester'] = 'Atanas Stankin'


@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop('Plugins', None)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = os.path.abspath(os.curdir) + '\\reports\\' + datetime.now().strftime(
        "%d-%m-%Y %H-%M-%S") + ".html"

# def open_form(setup, base_url, logger, login_username, login_password):
#     driver = setup
#     driver.get(base_url)
#     logger.info("Launching application")
#     driver.maximize_window()
#
#     logger.info("click on [Sign in]")
#     index_page = IndexPage(driver)
#     index_page.click_sign_in()
#
#     logger.info("Providing customer details for login")
#     login_page = LoginPage(driver)
#     login_page.set_username(login_username)
#     login_page.set_password(login_password)
#     login_page.click_sign_in()
#
#     logger.info("Loading home page")
