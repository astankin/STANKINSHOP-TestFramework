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

    def __init__(self, driver):
        self.driver = driver

    def get_name_input(self):
        return self.driver.find_element(By.ID, self.name_input_id)

    def get_email_input(self):
        return self.driver.find_element(By.ID, self.email_input_id)

    def get_password_input(self):
        return self.driver.find_element(By.ID, self.password_input_id)

    def get_conf_password_input(self):
        return self.driver.find_element(By.ID, self.conf_pass_input_id)

    def get_register_btn(self):
        return self.driver.find_element(By.XPATH, self.register_btn_xpath)

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
        pass

    def get_email_error_msg(self):
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.email_input_id))).get_attribute("validationMessage")
        return message

    def register(self, name, email, password, conf_password):
        self.set_name(name)
        self.set_email(email)
        self.set_password(password)
        self.set_conf_password(conf_password)
        self.click_register_btn()
