from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductListPage:
    url = 'http://127.0.0.1:8000/#/admin/productlist'
    create_product_btn = '//*[@id="root"]/main/div/div/div[1]/div[2]/button'
    last_product_name = '//*[@id="root"]/main/div/div/div[2]/div/table/tbody/tr[1]/td[2]/a'

    def __init__(self, driver):
        self.driver = driver

    def get_create_product_btn(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.create_product_btn)))

    def click_create_product_btn(self):
        self.get_create_product_btn().click()