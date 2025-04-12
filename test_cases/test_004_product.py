from time import sleep

import pytest
from selenium.webdriver.common.by import By

from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from page_objects.profile_page import ProfilePage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig


class TestProduct:
    base_url = ProductPage.url
    logger = setup_logger(log_file_path='logs/test_product.log')
    login_email = ReadConfig.get_email()
    login_password = ReadConfig.get_password()
    login_name = ReadConfig.get_name()
    option = "4 - Very Good"
    comment = 'Very good product.'

    @pytest.fixture()
    def preconditions(self, setup):
        self.driver = setup
        self.login_page = LoginPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.driver.get(self.login_page.url)
        self.logger.info("Launching application")
        self.driver.maximize_window()
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.login_email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        self.driver.get(self.base_url)


    def test_add_rating(self, preconditions):
        self.product_page.select_rating_option(self.option)
        self.product_page.insert_comment(self.comment)
        sleep(3)
        # self.product_page.click_on_submit_btn()
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary')
        self.driver.execute_script("arguments[0].click();", submit_button)
        rating = self.product_page.get_rating()
        if len(rating) == 13:
            assert True, "Test passed: 4 stars are displayed correctly."
        else:
            pytest.fail(f"Test failed: Expected {13} stars, but found {len(rating)}.")

    def test_review_product_already_reviewed(self, preconditions):
        self.product_page.select_rating_option(self.option)
        self.product_page.insert_comment(self.comment)
        sleep(3)
        # self.product_page.click_on_submit_btn()
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"].btn.btn-primary')
        self.driver.execute_script("arguments[0].click();", submit_button)
        expected_msg = 'Product already reviewed'
        try:
            error_msg = self.product_page.get_reviewed_msg()
            assert error_msg.text == expected_msg
        except Exception as ex:
            pytest.fail(f'{ex}')

    def test_add_product_to_cart(self, setup, preconditions):
        sleep(2)
        self.product_page.click_on_add_to_cart()
        sleep(2)


