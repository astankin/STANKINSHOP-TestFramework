import os
from time import sleep
import random

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.common import NoSuchElementException

# from selenium.common import NoSuchElementException

from page_objects.home_page import HomePage
from page_objects.index_page import IndexPage
# from page_objects.login_page import LoginPage
from page_objects.register_page import RegisterPage
# from page_objects.users_list_page import UsersListPage
from utilities.custom_logger import setup_logger
from utilities.email_generator import generate_random_email
# from utilities.get_db_data import UserData
# from utilities.password_generator import generate_random_password
from utilities.read_properties import ReadConfig
from utilities.username_generator import generate_random_username


class TestAccountRegister:
    base_url = RegisterPage.url
    logger = setup_logger(log_file_path='logs/register_account.log')
    login_name = ReadConfig.get_name()
    login_password = ReadConfig.get_password()
    name = generate_random_username(5)
    email = name + "@yahoo.com"
    password = ReadConfig.get_password()
    conf_password = ReadConfig.get_password()
    chars = ReadConfig.get_chars_list()
    COMMON_PASSWORDS = ['password',
                        'qwertyui',
                        'abcdefgh',
                        'letmein1',
                        'admin123',
                        'monkey12',
                        'sunshine',
                        'football',
                        'password1',
                        'welcome1']

    def preconditions(self, setup):
        self.driver = setup
        self.driver.get(self.base_url)
        self.logger.info("Launching application")
        self.driver.maximize_window()
        self.register_page = RegisterPage(self.driver)
        self.home_page = HomePage(self.driver)

    def test_name_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        name_label = self.register_page.get_name_label()
        assert name_label == 'Name', f"Expected 'Name', but got {name_label}"

    def test_email_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        email_label = self.register_page.get_email_label()
        assert email_label == 'Email Address', f"Expected 'Email', but got {email_label}"

    def test_password_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        password_label = self.register_page.get_password_label()
        assert password_label == 'Password', f"Expected 'Password', but got {password_label}"

    def test_conf_password_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        conf_password_label = self.register_page.get_conf_pass_label()
        assert conf_password_label == 'Confirm Password', f"Expected 'Confirm Password', but got {conf_password_label}"

    def test_name_input_field(self, setup):
        self.preconditions(setup)
        input_element = self.register_page.get_name_input()
        assert input_element.get_attribute("type") == "text", "Input field is not of type 'text'"

    def test_email_input_field(self, setup):
        self.preconditions(setup)
        input_element = self.register_page.get_email_input()
        assert input_element.get_attribute("type") == "email", "Input field is not of type 'email'"

    def test_password_input_field(self, setup):
        self.preconditions(setup)
        input_element = self.register_page.get_email_input()
        assert input_element.get_attribute("type") == "password", "Input field is not of type 'password'"

    def test_conf_password_input_field(self, setup):
        self.preconditions(setup)
        input_element = self.register_page.get_conf_password_input()
        assert input_element.get_attribute("type") == "password", "Input field is not of type 'password'"

    def test_register_btn(self, setup):
        self.preconditions(setup)
        input_element = self.register_page.get_register_btn()
        assert input_element.get_attribute("type") == "submit", "Input field is not of type 'submit'"

    def test_account_register_with_valid_data(self, setup):
        self.preconditions(setup)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        sleep(3)
        user_link = self.home_page.get_user_link()
        assert self.driver.current_url == self.home_page.url
        assert user_link.is_displayed()

    def test_register_user_with_name_less_then_4(self, setup):
        self.logger.info("Starting test with username less then 4 chars")
        self.preconditions(setup)
        self.name = generate_random_username(3)
        self.email = self.name + '@mail.com'
        self.register_page.register(self.name, self.email, self.password, self.conf_password)

        expected_message = f"Ensure this value has at least 4 characters (it has {len(self.name)})."
        try:
            message = self.register_page.get_name_error_msg()
            assert message.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
            assert expected_message == message
        except NoSuchElementException:
            raise AssertionError("The username can NOT be less then 4 characters")

    def test_register_user_with_empty_name(self, setup):
        self.preconditions(setup)
        self.name = ""
        self.email = generate_random_email()
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = f"Please fill out this field."
        try:
            # Verify the validation message
            message = self.register_page.get_name_error_msg()
            assert expected_message == message
        except NoSuchElementException:
            allure.attach(self.driver.get_screenshot_as_png(), name="test_empty_name",
                          attachment_type=AttachmentType.PNG)
            raise AssertionError("The name field can NOT be empty")

    def test_register_name_with_numbers_only(self, setup):
        self.preconditions(setup)
        self.name = random.randint(100000, 999999)
        self.email = generate_random_email()

        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = f"Account for {self.name} created successfully."
        sleep(3)
        try:
            current_url = self.driver.current_url
            # Assert that the user is not registered
            assert current_url != self.home_page.url
        except NoSuchElementException:
            assert False

 ########################### Testing Registration Email Field ########################################
    def test_register_user_with_empty_email(self, setup):
        self.preconditions(setup)
        self.email = ""
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "Please fill out this field."
        try:
            # Verify the validation message
            message = self.register_page.get_email_error_msg()
            assert expected_message == message, "The email field can NOT be empty!"
        except NoSuchElementException:
            raise AssertionError("The email field can NOT be empty!")

    @pytest.mark.sanity
    def test_register_user_with_email_without_at_symbol(self, setup):
        self.preconditions(setup)
        self.email = "john.doe.gmail.com"
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = f"Please include an '@' in the email address. '{self.email}' is missing an '@'."
        sleep(3)
        try:
            message = self.register_page.get_email_error_msg()
            assert expected_message == message
            assert self.driver.current_url == self.register_page.url
        except NoSuchElementException:
            raise AssertionError("The email field must contains '@' symbol!")

    # def test_register_user_with_email_without_domain(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email without domain ****")
    #     self.email = "john.doe@gmail"
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"Enter a valid email address."
    #     try:
    #         message = self.register_page.get_email_error_msg().text
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email field can contains domain!")
    #
    # def test_register_user_with_email_without_name(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email withouth @ symbol ****")
    #     self.email = "@" + generate_random_email().split('@')[1]
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"Please enter a part followed by '@'. '{self.email}' is incomplete."
    #     try:
    #         message = self.register_page.get_email_validation_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email can NOT be without a name!")
    #
    # def test_register_user_with_more_then_one_domain(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email withouth @ symbol ****")
    #     self.email = generate_random_email() + ".co.uk"
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"Account for {self.username} created successfully."
    #     try:
    #         message = self.register_page.get_confirm_message()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email can contains more then one domains!")
    #
    # def test_register_user_with_email_more_then_one_at_symbols(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email contain more then one @ symbol ****")
    #     self.email = generate_random_email() + "@" + ".co.uk"
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"A part following '@' should not contain the symbol '@'."
    #     try:
    #         message = self.register_page.get_email_validation_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email can NOT contains more then one @ symbols!")
    #
    # def test_register_user_with_email_contains_special_char(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email contains special char ****")
    #     not_allowed_chars = []
    #     base_email = generate_random_username(5)
    #     domain = '@yahoo.com'
    #     emails = [base_email + char for char in self.chars if char not in ["_", "-", "."]]
    #     for email in emails:
    #         self.username = generate_random_username(6)
    #         self.email = email + domain
    #         self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                     self.password, self.conf_password)
    #
    #         expected_message = f"A part followed by '@' should not contain the symbol '{email[-1]}'."
    #         try:
    #             message_element = self.register_page.get_email_validation_msg()
    #             assert expected_message == message_element
    #         except:
    #             not_allowed_chars.append(email[-1])
    #         self.home_page = HomePage(self.driver)
    #         self.home_page.click_on_create_user()
    #     if len(not_allowed_chars) > 0:
    #         raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")
    #
    # def test_register_user_with_email_name_contains_white_space(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email name contain white space ****")
    #     self.email = generate_random_username(3) + " " + generate_random_email()
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"A part followed by '@' should not contain the symbol ' '."
    #     try:
    #         message = self.register_page.get_email_validation_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email can NOT contains more then one @ symbols!")
    #
    # def test_register_user_with_email_name_contains_only_numbers(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email name contain white space ****")
    #     self.email = str(random.randint(100000, 999999)) + "@" + "yahoo.com"
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"Enter a valid email address."
    #     try:
    #         message = self.register_page.get_email_error_msg()
    #         assert expected_message == message.text
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email name can not contains only numbers")
    #
    # def test_register_user_with_email_domain_name_contains_only_numbers(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email domain name contain white space ****")
    #     self.email = 'john.doe' + "@" + str(random.randint(100000, 999999)) + ".com"
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"Enter a valid email address."
    #     try:
    #         message = self.register_page.get_email_error_msg()
    #         assert expected_message == message.text
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email domain name can not contains only numbers")
    #
    # def test_register_user_with_email_name_domain_name_and_domain_contains_only_numbers(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with email name contain white space ****")
    #     self.email = str(random.randint(100000, 999999)) + "@" + \
    #                  str(random.randint(100000, 999999)) + "." + \
    #                  str(random.randint(100000, 999999))
    #     self.username = generate_random_username(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = f"Enter a valid email address."
    #     try:
    #         message = self.register_page.get_email_error_msg()
    #         assert expected_message == message.text
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The email name, domain name and domain can not contains only numbers")
    #
    # #################### Testing Password Field ########################################################
    #
    # def test_register_user_with_password_similar_to_username(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with password less then 8 chars long ****")
    #     self.username = generate_random_username(9)
    #     self.email = generate_random_email()
    #     self.password = self.username
    #     self.conf_password = self.username
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "The password is too similar to the username."
    #     try:
    #         message = self.register_page.get_password_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The password can’t be too similar to your other personal information.")
    #
    # def test_register_user_with_password_less_then_8_chars(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with less then 8 characters ****")
    #     self.username = generate_random_username(6)
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(7)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "This password is too short. It must contain at least 8 characters."
    #     try:
    #         message = self.register_page.get_password_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The password can’t be too similar to your other personal information.")
    #
    # def test_register_user_with_too_common_password(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with too common password ****")
    #     for password in self.COMMON_PASSWORDS:
    #         self.username = generate_random_username(6)
    #         self.email = generate_random_email()
    #         self.password = password
    #         self.conf_password = password
    #         self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                     self.password, self.conf_password)
    #         self.driver = setup
    #         expected_message = "This password is too common."
    #         try:
    #             message = self.register_page.get_password_error_msg()
    #             assert message.is_displayed()
    #             assert expected_message == message.text
    #         except:
    #             allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                           attachment_type=AttachmentType.PNG)
    #             raise AssertionError("The password is too common!")
    #         self.home_page = HomePage(self.driver)
    #         self.home_page.click_on_create_user()
    #
    # def test_register_user_with_confirm_password_mismatch_the_password(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with confirm password different then password ****")
    #     self.username = generate_random_username(6)
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = generate_random_password(7)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "The two password fields didn’t match."
    #     try:
    #         message = self.register_page.get_password_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The two passwords must be same")
    #
    # @pytest.mark.current
    # def test_register_user_with_password_length_40_char(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.logger.info("**** Test register user with confirm password different then password ****")
    #     self.username = generate_random_username(6)
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(40)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "The password is too long."
    #     try:
    #         message = self.register_page.get_password_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_with_empty_email_field",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The password can NOT be longer then 20 characters")
    #
    # def test_register_user_with_empty_conf_password(self, setup):
    #     self.logger.info("Starting test with empty confirmation password")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.email = generate_random_email()
    #     self.conf_password = ""
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "Please fill out this field."
    #     try:
    #         # Verify the validation message
    #         message = self.register_page.get_conf_password_validation_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_username_less_then_5",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The username can NOT be less then 4 characters")
    #
    # def test_register_user_verify_masked_password(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.email = generate_random_email()
    #     self.register_page.set_username(self.username)
    #     self.register_page.set_email(self.email)
    #     self.register_page.set_password(self.password)
    #     password_input = self.register_page.get_password()
    #     assert password_input.get_attribute("type") == "password"
    #
    # def test_register_user_verify_masked_password(self, setup):
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.email = generate_random_email()
    #     self.register_page.set_username(self.username)
    #     self.register_page.set_email(self.email)
    #     self.register_page.set_password(self.password)
    #     conf_password_input = self.register_page.get_conf_password()
    #     assert conf_password_input.get_attribute("type") == "password"
    #
    # def test_register_user_with_password_contains_only_numbers(self, setup):
    #     self.logger.info("Starting test with password entirely numeric")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.email = generate_random_email()
    #     self.password = random.randint(10000000, 99999999)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "This password is entirely numeric."
    #     try:
    #         # Verify the validation message
    #         message = self.register_page.get_password_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_username_less_then_5",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The password can NOT be entirely numeric.")
    #
    # def test_register_user_with_password_contains_white_space(self, setup):
    #     self.logger.info("Starting test with password contains white space")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(4) + " " + generate_random_password(4)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.driver = setup
    #     expected_message = "This is invalid password"
    #     try:
    #         message = self.register_page.get_password_error_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The password can NOT contains white space.")
    #
    # def test_create_plant_with_valid_data_click_cancel(self, setup):
    #     self.open_register_form(setup)
    #     self.home_page.click_on_users_list()
    #     self.user_list_page = UsersListPage(self.driver)
    #     last_created_user = self.user_list_page.get_last_created_user_name()
    #
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.home_page.click_on_create_user()
    #     self.username = generate_random_username(7)
    #     self.email = generate_random_email()
    #     self.register_page.set_username(self.username)
    #     self.register_page.set_email(self.email)
    #     self.register_page.select_role(self.role)
    #     self.register_page.set_password(self.password)
    #     self.register_page.set_confirm_password(self.password)
    #     self.register_page.click_cancel_btn()
    #
    #     self.home_page.click_on_users_list()
    #     last_user = self.user_list_page.get_last_created_user_name()
    #
    #     if last_created_user == last_user:
    #         self.logger.info("Registration PASSED")
    #         assert True
    #     else:
    #         screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
    #         screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
    #         self.driver.save_screenshot(screenshot_path)
    #         self.logger.info("Registration FAILED")
    #         assert False
    #
    # ##########################################################################################################
    # # Testing First Name
    #
    # def test_register_user_with_empty_firstname_input_field(self, setup):
    #     self.logger.info("Starting test with empty firstname input field")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.first_name = ""
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = "Please fill out this field."
    #     try:
    #         message = self.register_page.get_first_name_error_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("The first name field can not be empty.")
    #
    # def test_register_user_with_firstname_contains_numbers(self, setup):
    #     self.logger.info("Starting test with firstname contains numbers")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.first_name = "123Atanas"
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = "Only letters are allowed"
    #     try:
    #         message = self.register_page.get_first_name_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("First name can contains only letters.")
    #
    # def test_register_user_with_first_name_contains_special_char(self, setup):
    #     self.open_register_form(setup)
    #     self.logger.info("**** Test register user with first name contains special chars ****")
    #     self.register_page = RegisterUserPage(self.driver)
    #     first_name_with_char = [self.first_name + str(char) for char in self.chars]
    #     not_allowed_chars = []
    #     for f_name in first_name_with_char:
    #         self.email = generate_random_email()
    #         self.username = generate_random_username(5)
    #         self.register_page.register(self.username, self.email, f_name, self.last_name, self.role, self.password,
    #                                     self.conf_password)
    #
    #         expected_message = f"Only letters are allowed"
    #         try:
    #             message_element = self.register_page.get_first_name_error_msg()
    #             assert message_element.is_displayed()
    #             assert expected_message == message_element.text
    #         except NoSuchElementException:
    #             not_allowed_chars.append(f_name[-1])
    #         self.home_page = HomePage(self.driver)
    #         self.home_page.click_on_create_user()
    #     if len(not_allowed_chars) > 0:
    #         raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")
    #
    # def test_register_user_with_firstname_contains_white_space(self, setup):
    #     self.logger.info("Starting test with firstname contains numbers")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.first_name = "Ata nas"
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = "Only letters are allowed"
    #     try:
    #         message = self.register_page.get_first_name_error_msg().text
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("First name can contains only letters.")
    #
    # def test_register_user_with_firstname_length_less_then_2(self, setup):
    #     self.logger.info("Starting test with firstname less then 2 letters")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.first_name = "A"
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = f"Ensure this value has at least 2 characters (it has {len(self.first_name)})."
    #     try:
    #         message = self.register_page.get_first_name_error_msg().text
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("Ensure this value has at least 2 characters.")
    #
    # def test_register_user_with_firstname_leading_white_space_trim(self, setup):
    #     self.open_register_form(setup)
    #     self.first_name = "  Atanas"
    #     self.logger.info("Loading register page")
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.confirm_msg = self.register_page.get_confirm_message()
    #
    #     if self.confirm_msg == f"Account for {self.username} created successfully.":
    #         self.logger.info("Registration PASSED")
    #         assert True
    #     else:
    #         screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
    #         screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
    #         self.driver.save_screenshot(screenshot_path)
    #         self.logger.info("Registration FAILED")
    #         assert False
    #     user_data = UserData()
    #     user_id = user_data.get_last_user_id()
    #     first_name = user_data.get_first_name(user_id)
    #     assert self.first_name.strip() == first_name
    #
    # def test_register_user_with_firstname_tailing_white_space_trim(self, setup):
    #     self.open_register_form(setup)
    #     self.first_name = "Atanas  "
    #     self.logger.info("Loading register page")
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.confirm_msg = self.register_page.get_confirm_message()
    #
    #     if self.confirm_msg == f"Account for {self.username} created successfully.":
    #         self.logger.info("Registration PASSED")
    #         assert True
    #     else:
    #         screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
    #         screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
    #         self.driver.save_screenshot(screenshot_path)
    #         self.logger.info("Registration FAILED")
    #         assert False
    #     user_data = UserData()
    #     user_id = user_data.get_last_user_id()
    #     first_name = user_data.get_first_name(user_id)
    #     assert self.first_name.strip() == first_name
    #
    # #################################################################################################
    # # Testing Last Name
    #
    # def test_register_user_with_empty_lastname_input_field(self, setup):
    #     self.logger.info("Starting test with empty last name input field")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.last_name = ""
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = "Please fill out this field."
    #     try:
    #         message = self.register_page.get_last_name_validation_msg()
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("Last name field can not be empty.")
    #
    # def test_register_user_with_last_name_contains_numbers(self, setup):
    #     self.logger.info("Starting test with firstname contains numbers")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.last_name = "123Stankin"
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = "Only letters are allowed"
    #     try:
    #         message = self.register_page.get_last_name_error_msg()
    #         assert message.is_displayed()
    #         assert expected_message == message.text
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("First name can contains only letters.")
    #
    # def test_register_user_with_last_name_contains_special_char(self, setup):
    #     self.open_register_form(setup)
    #     self.logger.info("**** Test register user with first name contains special chars ****")
    #     self.register_page = RegisterUserPage(self.driver)
    #     last_name_with_char = [self.first_name + str(char) for char in self.chars]
    #     not_allowed_chars = []
    #     for l_name in last_name_with_char:
    #         self.email = generate_random_email()
    #         self.username = generate_random_username(5)
    #         self.register_page.register(self.username, self.email, self.first_name, l_name, self.role, self.password,
    #                                     self.conf_password)
    #
    #         expected_message = f"Only letters are allowed"
    #         try:
    #             message_element = self.register_page.get_last_name_error_msg()
    #             assert message_element.is_displayed()
    #             assert expected_message == message_element.text
    #         except NoSuchElementException:
    #             not_allowed_chars.append(l_name[-1])
    #         self.home_page = HomePage(self.driver)
    #         self.home_page.click_on_create_user()
    #     if len(not_allowed_chars) > 0:
    #         raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")
    #
    # def test_register_user_with_last_name_contains_white_space(self, setup):
    #     self.logger.info("Starting test with firstname contains numbers")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.last_name = "Sta nkin"
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = "Only letters are allowed"
    #     try:
    #         message = self.register_page.get_last_name_error_msg().text
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("Last name can contains only letters.")
    #
    # def test_register_user_with_last_name_length_less_then_2(self, setup):
    #     self.logger.info("Starting test with last name less then 2 letters")
    #     self.open_register_form(setup)
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.username = generate_random_username(7)
    #     self.last_name = "A"
    #     self.email = generate_random_email()
    #     self.password = generate_random_password(8)
    #     self.conf_password = self.password
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     expected_message = f"Ensure this value has at least 2 characters (it has {len(self.last_name)})."
    #     try:
    #         message = self.register_page.get_last_name_error_msg().text
    #         assert expected_message == message
    #     except NoSuchElementException:
    #         allure.attach(self.driver.get_screenshot_as_png(), name="test_password",
    #                       attachment_type=AttachmentType.PNG)
    #         raise AssertionError("Ensure this value has at least 2 characters.")
    #
    # def test_register_user_with_last_name_leading_white_space_trim(self, setup):
    #     self.open_register_form(setup)
    #     self.last_name = "  Atanas"
    #     self.logger.info("Loading register page")
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.confirm_msg = self.register_page.get_confirm_message()
    #
    #     if self.confirm_msg == f"Account for {self.username} created successfully.":
    #         self.logger.info("Registration PASSED")
    #         assert True
    #     else:
    #         screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
    #         screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
    #         self.driver.save_screenshot(screenshot_path)
    #         self.logger.info("Registration FAILED")
    #         assert False
    #     user_data = UserData()
    #     user_id = user_data.get_last_user_id()
    #     last_name = user_data.get_last_name(user_id)
    #     assert self.first_name.strip() == last_name
    #
    # def test_register_user_with_last_name_tailing_white_space_trim(self, setup):
    #     self.open_register_form(setup)
    #     self.last_name = "Atanas  "
    #     self.logger.info("Loading register page")
    #     self.register_page = RegisterUserPage(self.driver)
    #     self.register_page.register(self.username, self.email, self.first_name, self.last_name, self.role,
    #                                 self.password, self.conf_password)
    #     self.confirm_msg = self.register_page.get_confirm_message()
    #
    #     if self.confirm_msg == f"Account for {self.username} created successfully.":
    #         self.logger.info("Registration PASSED")
    #         assert True
    #     else:
    #         screenshot_dir = os.path.abspath(os.curdir) + "\\screenshots"
    #         screenshot_path = os.path.join(screenshot_dir, "test_account_register.png")
    #         self.driver.save_screenshot(screenshot_path)
    #         self.logger.info("Registration FAILED")
    #         assert False
    #     user_data = UserData()
    #     user_id = user_data.get_last_user_id()
    #     last_name = user_data.get_last_name(user_id)
    #     assert self.last_name.strip() == last_name
