from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    url = "http://127.0.0.1:8000/#/login"
    email_field_xpath = "//*[@id='email']"
    password_field_xpath = '//*[@id="password"]'
    btn_signin_xpath = '//*[@id="root"]/main/div/div/div/div/form/button'
    register_linc_xpath = '//*[@id="root"]/main/div/div/div/div/div/div/a'
    login_error_msg = '//*[@id="root"]/main/div/div/div/div/div[1]'

    def __init__(self, driver):
        self.driver = driver

    def get_email_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.email_field_xpath)))

    def get_password_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.password_field_xpath)))

    def set_email(self, email):
        self.get_email_input().send_keys(email)

    def set_password(self, password):
        self.get_password_input().send_keys(password)

    def click_signin(self):
        self.driver.find_element(By.XPATH, self.btn_signin_xpath).click()

    def register_link_click(self):
        self.driver.find_element(By.XPATH, self.register_linc_xpath).click()

    def get_error_message(self):
        return self.driver.find_element(By.XPATH, self.login_error_msg)

    def get_email_error_msg(self):
        try:
            message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.email_field_xpath))).get_attribute("validationMessage")
            return message
        except NoSuchElementException as e:
            raise AssertionError(f"{e}")

