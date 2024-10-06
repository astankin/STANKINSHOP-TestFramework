from time import sleep
import random

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.common import NoSuchElementException, TimeoutException

from page_objects.home_page import HomePage
from page_objects.register_page import RegisterPage
from utilities.custom_logger import setup_logger
from utilities.email_generator import generate_random_email
from utilities.password_generator import generate_random_password
from utilities.read_properties import ReadConfig
from utilities.username_generator import generate_random_username


class TestAccountRegister:
    base_url = RegisterPage.url
    logger = setup_logger(log_file_path='logs/register_account.log')
    login_name = ReadConfig.get_name()
    login_email = ReadConfig.get_email()
    login_password = ReadConfig.get_password()
    name = generate_random_username(5)
    email = name + "@yahoo.com"
    password = ReadConfig.get_password()
    conf_password = ReadConfig.get_password()
    chars = ReadConfig.get_chars_list()
    common_passwords = ReadConfig.get_common_passwords_list()

    def preconditions(self, setup):
        self.driver = setup
        self.driver.get(self.base_url)
        self.logger.info("Launching application")
        self.driver.maximize_window()
        self.register_page = RegisterPage(self.driver)
        self.home_page = HomePage(self.driver)

    def test_name_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test name label ****")
        name_label = self.register_page.get_name_label()
        assert name_label == 'Name', f"Expected 'Name', but got {name_label}"

    def test_email_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test email label ****")
        email_label = self.register_page.get_email_label()
        assert email_label == 'Email Address', f"Expected 'Email', but got {email_label}"

    def test_password_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test name Password label ****")
        password_label = self.register_page.get_password_label()
        assert password_label == 'Password', f"Expected 'Password', but got {password_label}"

    def test_conf_password_label_exists_and_correct_spelling(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test Confirm Password label ****")
        conf_password_label = self.register_page.get_conf_pass_label()
        assert conf_password_label == 'Confirm Password', f"Expected 'Confirm Password', but got {conf_password_label}"

    def test_name_input_field(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test name input field ****")
        input_element = self.register_page.get_name_input()
        assert input_element.get_attribute("type") == "text", "Input field is not of type 'text'"

    def test_email_input_field(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test email input field ****")
        input_element = self.register_page.get_email_input()
        assert input_element.get_attribute("type") == "email", "Input field is not of type 'email'"

    def test_password_input_field(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test password input field type password****")
        input_element = self.register_page.get_password_input()
        assert input_element.get_attribute("type") == "password", "Input field is not of type 'password'"

    def test_conf_password_input_field(self, setup):
        self.preconditions(setup)
        self.logger.info("**** Test Confirm Password input field type password****")
        input_element = self.register_page.get_conf_password_input()
        assert input_element.get_attribute("type") == "password", "Input field is not of type 'password'"

    def test_register_btn(self, setup):
        self.preconditions(setup)
        input_element = self.register_page.get_register_btn()
        assert input_element.get_attribute("type") == "submit", "Input field is not of type 'submit'"

    def test_account_register_with_valid_data(self, setup):
        self.preconditions(setup)
        self.email = generate_random_email()
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        sleep(3)
        user_link = self.home_page.get_user_link()
        assert self.driver.current_url == self.home_page.url
        assert user_link.is_displayed()

    def test_account_register_with_existing_user(self, setup):
        self.preconditions(setup)
        self.register_page.register(self.login_name, self.login_email, self.password, self.conf_password)
        sleep(3)
        expected_message = 'User with this email already exists'
        error_message = self.register_page.get_register_error_msg()
        assert expected_message == error_message.text
        assert error_message.is_displayed()
        assert self.driver.current_url == self.register_page.url

    def test_register_user_with_name_less_then_4(self, setup):
        self.logger.info("Starting test with username less then 4 chars")
        self.preconditions(setup)
        self.name = generate_random_username(3)
        self.email = self.name + '@mail.com'
        self.register_page.register(self.name, self.email, self.password, self.conf_password)

        expected_message = f"Ensure this value has at least 4 characters (it has {len(self.name)})."
        message = self.register_page.get_name_validation_msg()
        if not message:
            pytest.fail("The error message is not displayed. The username can NOT be less then 4 characters")
        assert message.is_displayed(), f"Expected message: '{expected_message}' not found on the page."
        assert expected_message == message

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

    def test_register_user_with_email_without_at_symbol(self, setup):
        self.preconditions(setup)
        self.email = "john.doe.gmail.com"
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = f"Please include an '@' in the email address. '{self.email}' is missing an '@'."
        message = self.register_page.get_email_error_msg()
        if not message:
            pytest.fail("The error message is not displayed")
        assert message == expected_message, f"Expected message: {expected_message}, but got: {message}"
        assert self.driver.current_url == self.register_page.url, \
            f"Expected to be {self.register_page.url}, but got {self.driver.current_url}"

    def test_register_user_with_email_without_domain(self, setup):
        self.preconditions(setup)
        self.email = "john.doe@gmail"
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "Please enter a valid email address."
        error_message = self.register_page.get_email_validation_msg()
        if not error_message:
            pytest.fail("The error message is not displayed")
        assert error_message.text == expected_message, f"Expected message: {expected_message}, but got: {error_message}"
        assert self.driver.current_url == self.register_page.url, \
            f"Expected to be {self.register_page.url}, but got {self.driver.current_url}"

    def test_register_user_with_email_without_name(self, setup):
        self.preconditions(setup)
        self.email = "@" + generate_random_email().split('@')[1]
        self.name = generate_random_username(7)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = f"Please enter a part followed by '@'. '{self.email}' is incomplete."
        error_message = self.register_page.get_email_error_msg()
        if not error_message:
            pytest.fail("The error message is not displayed")
        assert error_message == expected_message, f"Expected message: {expected_message}, but got: {error_message}"
        assert self.driver.current_url == self.register_page.url, \
            f"Expected to be {self.register_page.url}, but got {self.driver.current_url}"

    def test_register_user_with_more_then_one_domain(self, setup):
        self.preconditions(setup)
        self.email = generate_random_email() + ".co.uk"
        self.name = generate_random_username(7)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        self.driver = setup
        sleep(3)
        user_link = self.home_page.get_user_link()
        assert self.driver.current_url == self.home_page.url
        assert user_link.is_displayed()

    def test_register_user_with_email_more_then_one_at_symbols(self, setup):
        self.preconditions(setup)
        self.email = generate_random_email() + "@" + ".co.uk"
        self.name = generate_random_username(7)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "A part following '@' should not contain the symbol '@'."
        error_message = self.register_page.get_email_error_msg()
        if not error_message:
            pytest.fail("The error message is not displayed")
        assert expected_message == expected_message, f"Expected message: {expected_message}, but got: {error_message}"
        assert self.driver.current_url == self.register_page.url, \
            f"Expected to be {self.register_page.url}, but got {self.driver.current_url}"

    @pytest.mark.sanity
    def test_register_user_with_email_contains_special_characters(self, setup):
        self.preconditions(setup)
        self.name = generate_random_username(7)
        excluded_chars = ["_", "-", ".", "@"]
        not_allowed_chars = []
        for char in self.chars:
            if char in excluded_chars:
                continue
            self.email = f"{self.name}{char}@yahoo.com"
            self.register_page.register(self.name, self.email, self.password, self.conf_password)
            expected_message1 = f"A part followed by '@' should not contain the symbol '{char}'."
            expected_message2 = "Please enter a valid email address."
            sleep(3)
            if self.driver.current_url == self.home_page.url:
                not_allowed_chars.append(char)
                self.home_page.click_logout_link()
                self.driver.get(self.base_url)
                sleep(2)
                continue
            assert self.driver.current_url == self.register_page.url, \
                f"Expected to be {self.register_page.url}, but got {self.driver.current_url}"
            # reload the page
            self.driver.execute_script("location.reload(true);")
        if len(not_allowed_chars) == 0:
            assert True
        else:
            raise AssertionError(f"Test Failed! Characters: '{', '.join(not_allowed_chars)}' are not allowed")

    def test_register_user_with_email_name_contains_white_space(self, setup):
        self.preconditions(setup)
        self.email = generate_random_username(3) + " " + generate_random_email()
        self.name = generate_random_username(5)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "A part followed by '@' should not contain the symbol ' '."
        try:
            message = self.register_page.get_email_error_msg()
            assert expected_message == message
        except NoSuchElementException:
            raise AssertionError("The email can NOT contains more then one @ symbols!")

    def test_register_user_with_email_name_contains_only_numbers(self, setup):
        self.preconditions(setup)
        self.email = str(random.randint(100000, 999999)) + "@" + "yahoo.com"
        self.name = generate_random_username(7)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        sleep(3)
        expected_message = f"Enter a valid email address."
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The email name can not contains only numbers")
        message = self.register_page.get_email_error_msg()
        assert expected_message == message
        assert self.driver.current_url == self.base_url

    def test_register_user_with_email_domain_name_contains_only_numbers(self, setup):
        self.preconditions(setup)
        self.email = 'john.doe' + "@" + str(random.randint(100000, 999999)) + ".com"
        self.name = generate_random_username(7)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        sleep(3)
        expected_message = f"Enter a valid email address."
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The domain name can not contains only numbers")
        message = self.register_page.get_email_error_msg()
        assert expected_message == message
        assert self.driver.current_url == self.base_url

    # #################### Testing Password Field ########################################################

    def test_register_user_with_password_similar_to_username(self, setup):
        self.preconditions(setup)
        self.name = generate_random_username(9) + '@'
        self.email = generate_random_email()
        self.password = self.name
        self.conf_password = self.name
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "Password is too similar to your name."
        sleep(2)
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The password can not be too similar to the username")
        message = self.register_page.get_password_validation_msg()
        assert expected_message == message.text
        assert message.is_displayed()
        assert self.driver.current_url == self.base_url

    def test_register_user_with_password_less_then_8_chars(self, setup):
        self.preconditions(setup)
        self.name = generate_random_username(6)
        self.email = generate_random_email()
        self.password = generate_random_password(7)
        self.conf_password = self.password
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "Password must be at least 8 characters long."
        sleep(2)
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The password can not be less then 8 characters.")
        message = self.register_page.get_password_validation_msg()
        assert expected_message == message.text
        assert message.is_displayed()
        assert self.driver.current_url == self.base_url

    def test_register_user_with_confirm_password_mismatch_the_password(self, setup):
        self.preconditions(setup)
        self.email = generate_random_email()
        self.password = generate_random_password(9)
        self.conf_password = generate_random_password(9)
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "Passwords do not match."
        sleep(2)
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The passwords must be the same.")
        message = self.register_page.get_password_not_match_msg()
        assert expected_message == message.text
        assert message.is_displayed()
        assert self.driver.current_url == self.base_url

    def test_register_user_with_empty_conf_password(self, setup):
        self.preconditions(setup)
        self.email = generate_random_email()
        self.conf_password = ""
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        expected_message = "Please fill out this field."
        sleep(2)
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The passwords must be the same.")
        message = self.register_page.get_conf_pass_error_msg()
        assert expected_message == message
        assert self.driver.current_url == self.base_url

    def test_register_user_with_password_contains_only_numbers(self, setup):
        self.preconditions(setup)
        self.name = generate_random_username(7)
        self.email = generate_random_email()
        self.password = random.randint(10000000, 99999999)
        self.conf_password = self.password
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        self.driver = setup
        expected_message = "Password must contain at least one uppercase letter, " \
                           "one lowercase letter, one number, and one special character (!@#$%^&*?)"
        sleep(2)
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The password can not be entire numeric.")
        message = self.register_page.get_password_validation_msg()
        assert expected_message == message.text
        assert message.is_displayed()
        assert self.driver.current_url == self.base_url

    def test_register_user_with_password_contains_white_space(self, setup):
        self.preconditions(setup)
        self.name = generate_random_username(7)
        self.email = generate_random_email()
        self.password = generate_random_password(4) + " " + generate_random_password(4)
        self.conf_password = self.password
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        self.driver = setup
        expected_message = 'Password must not contain any spaces.'
        sleep(2)
        if self.driver.current_url == self.home_page.url:
            pytest.fail("The password can not contain any spaces.")
        message = self.register_page.get_password_validation_msg()
        assert expected_message == message.text
        assert message.is_displayed()
        assert self.driver.current_url == self.base_url

    def test_register_user_with_name_tailing_white_space_trim(self, setup):
        self.preconditions(setup)
        self.name = "Atanas  "
        self.register_page.register(self.name, self.email, self.password, self.conf_password)
        sleep(3)
        user_link = self.home_page.get_user_link()
        assert self.driver.current_url == self.home_page.url
        assert user_link.is_displayed()
        assert user_link.text == self.name.upper().strip()

