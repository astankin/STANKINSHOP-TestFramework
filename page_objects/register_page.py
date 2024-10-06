import pytest
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    url = 'http://127.0.0.1:8000/#/register'
    name_input_id = 'name'
    email_input_id = "email"
    password_input_id = "password"
    conf_pass_input_id = "passwordConfirm"
    name_label_xpath = '//*[@id="root"]/main/div/div/div/div/form/div[1]/label'
    email_label_xpath = '//*[@id="root"]/main/div/div/div/div/form/div[2]/label'
    password_label_xpath = '//*[@id="root"]/main/div/div/div/div/form/div[3]/label'
    conf_pass_label_xpath = '//*[@id="root"]/main/div/div/div/div/form/div[4]/label'
    register_btn_xpath = '//*[@id="root"]/main/div/div/div/div/form/button'
    sign_in_xpath = '//*[@id="root"]/main/div/div/div/div/div/div/a'
    password_validation_msg_xpath = "//*[@id='root']/main/div/div/div/div/form/div[3]/div[2]"
    email_validation_msg_xpath = "//*[@id='root']/main/div/div/div/div/form/div[2]/div"
    existing_user_error_msg = '//*[@id="root"]/main/div/div/div/div/div[1]'
    password_not_match_msg = '//*[@id="root"]/main/div/div/div/div/form/div[4]/div[2]'

    def __init__(self, driver):
        self.driver = driver

    def get_name_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.name_input_id)))

    def get_email_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.email_input_id)))

    def get_password_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.password_input_id)))

    def get_conf_password_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.conf_pass_input_id)))

    def get_sign_in(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.sign_in_xpath)))

    def get_register_btn(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.register_btn_xpath)))

    def get_register_error_msg(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.existing_user_error_msg)))

    def get_password_not_match_msg(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.password_not_match_msg)))

    def set_name(self, name):
        self.get_name_input().send_keys(name)

    def set_email(self, email):
        self.get_email_input().send_keys(email)

    def set_password(self, password):
        self.get_password_input().send_keys(password)

    def set_conf_password(self, conf_password):
        self.get_conf_password_input().send_keys(conf_password)

    def click_register_btn(self):
        self.get_register_btn().click()

    def click_sign_in(self):
        self.get_sign_in().click()

    def get_name_label(self):
        return self.driver.find_element(By.XPATH, self.name_label_xpath).text

    def get_email_label(self):
        return self.driver.find_element(By.XPATH, self.email_label_xpath).text

    def get_password_label(self):
        return self.driver.find_element(By.XPATH, self.password_label_xpath).text

    def get_conf_pass_label(self):
        return self.driver.find_element(By.XPATH, self.conf_pass_label_xpath).text

    def get_name_error_msg(self):
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.name_input_id))).get_attribute("validationMessage")
        return message

    def get_name_validation_msg(self):
        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'error_message'))).get_attribute("validationMessage")
            return message
        except NoSuchElementException as e:
            raise AssertionError(f"The error message is not displayed: {e}")

    def get_password_validation_msg(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.password_validation_msg_xpath))
        )

    def get_email_error_msg(self):
        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, self.email_input_id))).get_attribute("validationMessage")
            # message = self.driver.find_element(By.ID, self.email_input_id).get_attribute("validationMessage")
            return message
        except NoSuchElementException as e:
            raise AssertionError(f"{e}")

    def get_email_validation_msg(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.email_validation_msg_xpath))
        )

    def get_conf_pass_error_msg(self):
        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, self.conf_pass_input_id))).get_attribute("validationMessage")
            return message
        except NoSuchElementException as e:
            raise AssertionError(f"{e}")

    def clear_form_fields(self):
        self.get_name_input().clear()
        self.get_email_input().clear()
        self.get_password_input().clear()
        self.get_conf_password_input().clear()

    def register(self, name, email, password, conf_password):
        self.set_name(name)
        self.set_email(email)
        self.set_password(password)
        self.set_conf_password(conf_password)
        self.click_register_btn()
