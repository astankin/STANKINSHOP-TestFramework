import os
from time import sleep
import pytest
from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.profile_page import ProfilePage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig


class TestEditProfile:
    base_url = ProfilePage.url
    logger = setup_logger(log_file_path='logs/edit_user_profile.log')

    login_email = ReadConfig.get_email()
    login_password = ReadConfig.get_password()
    login_name = ReadConfig.get_name()

    # It must be changed every time when the test edit password is executed
    edit_password = 'Plovdiv8304@'

    @pytest.fixture()
    def preconditions(self, setup):
        self.driver = setup
        self.login_page = LoginPage(self.driver)
        self.home_page = HomePage(self.driver)
        self.profile_page = ProfilePage(self.driver)
        self.driver.get(self.login_page.url)
        self.logger.info("Launching application")
        self.driver.maximize_window()
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.login_email)
        self.login_page.set_password(self.login_password)
        self.login_page.click_signin()
        self.home_page.click_profile_link()

    def test_edit_user_name(self, setup, preconditions):
        name = self.profile_page.get_name_input().get_attribute('value').upper()
        self.profile_page.get_name_input().clear()
        edited_name = f'{name} EDITED'
        self.profile_page.set_name(edited_name)
        self.profile_page.click_update_btn()
        user_link = self.profile_page.get_user_link().text
        assert user_link == edited_name
        assert self.profile_page.get_name_input().get_attribute('value').upper() == edited_name

    def test_edit_email(self, setup, preconditions):
        self.profile_page.get_email_input().clear()
        edited_email = 'martin@mail.com'
        self.profile_page.set_email(edited_email)
        self.profile_page.click_update_btn()
        assert self.profile_page.get_email_input().get_attribute('value') == edited_email

    def test_edit_password(self, setup, preconditions):
        self.profile_page.set_password(self.edit_password)
        self.profile_page.set_conf_password(self.edit_password)
        self.profile_page.click_update_btn()
        self.profile_page.click_logout_link()
        self.driver.get(self.login_page.url)
        self.login_page.set_email(self.login_email)
        self.login_page.set_password(self.edit_password)
        self.login_page.click_signin()
        target_page = self.home_page.url
        user_link = self.home_page.get_user_link()
        try:
            assert self.driver.current_url == target_page, "The password is not changed! Please investigate!"
            assert user_link.is_displayed()
            assert user_link.text == self.login_name
        except BaseException:
            self.driver.save_screenshot(os.path.abspath(os.curdir) + "\\screenshots" + "\\test_login.png")
            assert False
        self.logger.info("**** End of test of edit password ****")
