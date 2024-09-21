from selenium.webdriver.common.by import By


class IndexPage:
    sign_in_xpath = "//*[@id='sign_in_btn']"

    def __init__(self, driver):
        self.driver = driver

    def click_sign_in(self):
        self.driver.find_element(By.XPATH, self.sign_in_xpath).click()
