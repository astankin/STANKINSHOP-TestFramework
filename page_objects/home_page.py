from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    url = 'http://127.0.0.1:8000/#/'
    link_user_xpath = '//*[@id="username"]'
    username_id = 'username'

    def __init__(self, driver):
        self.driver = driver

    def get_user_link(self):
        return self.driver.find_element(By.XPATH, self.link_user_xpath)

    def click_user_link(self):
        user_link = self.get_user_link()
        user_link.click()

    def click_logout_link(self):
        username_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.username_id))
        )
        username_link.click()
        logout_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_link.click()
