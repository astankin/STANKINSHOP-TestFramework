from selenium.webdriver.common.by import By


class HomePage:
    url = 'http://127.0.0.1:8000/#/'
    link_user_xpath = '//*[@id="username"]'

    def __init__(self, driver):
        self.driver = driver

    def get_user_link(self):
        return self.driver.find_element(By.XPATH, self.link_user_xpath)

    def click_user_link(self):
        user_link = self.get_user_link()
        user_link.click()

    # def clickRegister(self):
    #     self.driver.find_element(By.LINK_TEXT,self.lnk_register_linktext).click()
    #
    # def clickLogin(self):
    #     self.driver.find_element(By.LINK_TEXT,self.lnk_login_linktext).click()
