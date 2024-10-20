import os.path
from time import sleep

import allure
import pytest
from selenium.common import NoSuchElementException

from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.register_page import RegisterPage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig


class TestLogin:
    base_url = 'http://127.0.0.1:8000/'
    login_url = LoginPage.url
    logger = setup_logger(log_file_path='logs/register_account.log')

    login_email = ReadConfig.get_email()
    login_password = ReadConfig.get_password()
    # login_email = "martin@mail.com"
    # login_password = "Astankin83@"
    login_name = 'MARTIN EDITED'
    invalid_username = "username"
    invalid_password = "Password12"

    def preconditions(self, setup):
        self.driver = setup
        self.driver.get(self.login_url)
        self.logger.info("Launching application")
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)

    def test_login_with_valid_credentials(self, setup):
        self.preconditions(setup)
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.login_email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()

        target_page = self.home_page.url
        user_link = self.home_page.get_user_link()
        try:
            assert self.driver.current_url == target_page, "The user should be able to log in with valid credentials! Please investigate!"
            assert user_link.is_displayed()
            assert user_link.text == self.login_name
        except BaseException:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots" + "\\test_login.png")
            assert False
        self.logger.info("**** End of the login test with correct data ****")

    def test_login_with_invalid_credentials(self, setup):
        self.preconditions(setup)
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.invalid_username)
        self.login_page.set_password(self.invalid_password)
        self.login_page.click_signin()

        if self.driver.current_url == self.login_url:
            assert True
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots" + "\\test_login.png")
            assert False
        self.logger.info("**** End of the login test with invalid data ****")

    def test_login_with_invalid_username(self, setup):
        self.preconditions(setup)
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.invalid_username)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()

        if self.driver.current_url == self.login_url:
            assert True
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots" + "\\test_login.png")
            assert False
        self.logger.info("**** End of the login with invalid username ****")

    def test_login_with_invalid_password(self, setup):
        self.preconditions(setup)
        self.logger.info("Providing customer details for login")
        self.login_page = LoginPage(self.driver)
        self.login_page.set_email(self.login_email)
        self.login_page.set_password(self.invalid_password)
        self.login_page.click_signin()

        if self.driver.current_url == self.login_url:
            assert True
        else:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots" + "\\test_login.png")
            assert False
        self.logger.info("**** End of the login with invalid password ****")

    def test_login_with_empty_username(self, setup):
        self.preconditions(setup)
        self.login_page.set_email("")
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()

        expected_message = "Request failed with status code 400"
        try:
            # Verify the validation message
            message = self.login_page.get_error_message()
            assert message.is_displayed()
            assert expected_message == message.text
            assert self.driver.current_url == self.login_url
        except NoSuchElementException:
            raise AssertionError("The username can NOT be empty!")
        self.logger.info("**** End of the login with invalid username ****")

    def test_login_with_empty_password(self, setup):
        self.preconditions(setup)
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.login_email)
        self.login_page.set_password("")
        self.login_page.click_signin()
        expected_message = "Request failed with status code 400"
        try:
            # Verify the validation message
            message = self.login_page.get_error_message()
            assert message.is_displayed()
            assert expected_message == message.text
            assert self.driver.current_url == self.login_url
        except NoSuchElementException:
            raise AssertionError("The password can NOT be empty!")

        self.logger.info("**** End of the login with empty password ****")

    def test_login_with_empty_username_and_password(self, setup):
        self.preconditions(setup)
        self.login_page.set_email("")
        self.login_page.set_password("")
        self.login_page.click_signin()
        expected_message = "Request failed with status code 400"

        try:
            # Verify the validation message
            message = self.login_page.get_error_message()
            assert message.is_displayed()
            assert expected_message == message.text
            assert self.driver.current_url == self.login_url
        except NoSuchElementException:
            raise AssertionError("The password can NOT be empty!")

        self.logger.info("**** End of the login with empty username and empty password ****")

    def test_login_case_sensitive_email(self, setup):
        self.preconditions(setup)
        email = self.login_email.upper()
        self.login_page.set_email(email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        expected_message = "No active account found with the given credentials"
        sleep(2)
        try:
            # Verify the validation message
            message = self.login_page.get_error_message()
            assert self.driver.current_url == self.login_url, "The email must be case sensitive!"
            assert message.is_displayed()
            assert expected_message == message.text
        except NoSuchElementException:
            raise AssertionError("The email must be case sensitive!")

        self.logger.info("**** End of the login with empty username and empty password ****")

    def test_login_with_Cross_Site_Scripting(self, setup):
        self.preconditions(setup)
        email = "<script>alert('XSS')</script>"
        self.login_page.set_email(email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        expected_message = f"Please include an '@' in the email address. '{email}' is missing an '@'."
        sleep(2)
        try:
            # Verify the validation message
            message = self.login_page.get_email_error_msg()
            assert self.driver.current_url == self.login_url
            assert expected_message == message
        except NoSuchElementException:
            raise AssertionError("The email must be case sensitive!")

    def test_login_with_encoded_script_injection(self, setup):
        self.preconditions(setup)
        email = "%3Cscript%3Ealert('XSS')%3C%2Fscript%3E"
        self.login_page.set_email(email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        expected_message = f"Please include an '@' in the email address. '{email}' is missing an '@'."
        sleep(2)
        try:
            # Verify the validation message
            message = self.login_page.get_email_error_msg()
            assert self.driver.current_url == self.login_url
            assert expected_message == message
        except NoSuchElementException:
            raise AssertionError("The email must be case sensitive!")

    @pytest.mark.sanity
    def test_login_with_sql_injection(self, setup):
        self.preconditions(setup)
        email = "' OR '1'='1' --"
        self.login_page.set_email(email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        expected_message = f"Please include an '@' in the email address. '{email}' is missing an '@'."
        sleep(2)
        try:
            # Verify the validation message
            message = self.login_page.get_email_error_msg()
            assert self.driver.current_url == self.login_url
            assert expected_message == message
        except NoSuchElementException:
            raise AssertionError("The email must handle sql injection!")

    @pytest.mark.sanity
    def test_login_with_union_based_sql_injection(self, setup):
        self.preconditions(setup)
        email = "' UNION SELECT null, username, password FROM users --"
        self.login_page.set_email(email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        expected_message = f"Please include an '@' in the email address. '{email}' is missing an '@'."
        sleep(2)
        try:
            # Verify the validation message
            message = self.login_page.get_email_error_msg()
            assert self.driver.current_url == self.login_url
            assert expected_message == message
        except NoSuchElementException:
            raise AssertionError("The email must handle sql injection!")

    # f"Please include an '@' in the email address. '{self.email}' is missing an '@'."

    # def test_reset_password_link(self, setup):
    #     expected_url = "http://127.0.0.1:8000/user/password-reset/"
    #     self.open_login_form(setup)
    #     self.login_page = LoginPage(self.driver)
    #     link = self.login_page.get_reset_password_url()
    #     if link:
    #         self.login_page.click_on_reset_password_link()
    #         assert self.driver.current_url == expected_url
    #     else:
    #         raise AssertionError("Link is not present on the page.")

    def test_login_and_click_register_btn(self, setup):
        self.preconditions(setup)
        self.logger.info("Providing customer details for login")
        self.login_page.register_link_click()
        sleep(2)
        self.register_page = RegisterPage(setup)
        assert self.driver.current_url == 'http://127.0.0.1:8000/#/register?redirect=/'
