from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProfilePage:
    url = 'http://127.0.0.1:8000/#/profile'
    name_input_xpath = '//*[@id="name"]'
    email_input_xpath = '//*[@id="email"]'
    password_input_xpath = '//*[@id="password"]'
    conf_password_xpath = '//*[@id="passwordConfirm"]'
    update_btn_xpath = '//*[@id="root"]/main/div/div/div[1]/form/button'
    link_user_xpath = '//*[@id="username"]'

    def __init__(self, driver):
        self.driver = driver

    def get_name_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.name_input_xpath)))

    def get_email_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.email_input_xpath)))

    def get_password_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.password_input_xpath)))

    def get_conf_password_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.conf_password_xpath)))

    def get_update_btn(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.update_btn_xpath)))

    def set_name(self, name):
        self.get_name_input().send_keys(name)


    def set_email(self, email):
        self.get_email_input().send_keys(email)

    def set_password(self, password):
        self.get_password_input().send_keys(password)

    def set_conf_password(self, conf_password):
        self.get_conf_password_input().send_keys(conf_password)

    def click_update_btn(self):
        self.get_update_btn().click()

    def get_user_link(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.link_user_xpath))
        )
    def click_logout_link(self):
        self.get_user_link().click()
        logout_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_link.click()