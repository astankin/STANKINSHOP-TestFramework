from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EditProductPage:
    title_xpath = '//*[@id="root"]/main/div/div/div/div/div/h1'
    name_input_xpath = '//*[@id="name"]'
    price_input_xpath = '//*[@id="price"]'
    brand_input_xpath = '//*[@id="brand"]'
    stock_input_xpath = '//*[@id="countinstock"]'
    category_input_xpath = '//*[@id="category"]'
    description_input_xpath = '//*[@id="description"]'
    update_btn_xpath = '//*[@id="root"]/main/div/div/div/div/div/form/button'

    def __init__(self, driver):
        self.driver = driver

    def get_name_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.name_input_xpath)))

    def set_name(self, name):
        self.get_name_input().send_keys(name)

    def get_price_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.price_input_xpath)))

    def set_price(self, price):
       self.get_price_input().send_keys(price)

    def get_brand_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.brand_input_xpath)))

    def set_brand(self, brand):
        self.get_brand_input().send_keys(brand)

    def get_stock_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.stock_input_xpath)))

    def set_stock(self, quantity):
        self.get_stock_input().send_keys(quantity)

    def get_category_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.category_input_xpath)))

    def set_category(self, category):
        self.get_category_input().send_keys(category)

    def get_description_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.description_input_xpath)))

    def set_description(self, description):
        self.get_description_input().send_keys(description)

    def get_update_btn(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.update_btn_xpath)))

    def click_update_btn(self):
        self.get_update_btn().click()