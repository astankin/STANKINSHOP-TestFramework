from time import sleep

import pytest
from selenium.webdriver import ActionChains

from page_objects.edit_product_page import EditProductPage
from page_objects.login_page import LoginPage
from page_objects.product_list_page import ProductListPage
from page_objects.product_page import ProductPage
from utilities.custom_logger import setup_logger
from utilities.read_properties import ReadConfig


class TestCreateProduct:
    base_url = ProductListPage.url
    logger = setup_logger(log_file_path='logs/test_product.log')
    login_email = ReadConfig.get_email()
    login_password = ReadConfig.get_password()
    login_name = ReadConfig.get_name()
    admin_email = ReadConfig.get_admin_email()
    admin_password = ReadConfig.get_admin_password()
    product_name = 'Test Product'
    price = 29.99
    brand = 'Test Brand'
    quantity = 15
    category = 'Electronic'
    description = ('This electronic device is a compact, high-performance solution designed for modern users. '
                   'Featuring advanced circuitry and intuitive controls, '
                   'it delivers precise functionality and efficiency for both personal and professional applications. '
                   'Built with durability in mind, it ensures reliable performance in various environments.')

    @pytest.fixture()
    def preconditions(self, setup):
        self.driver = setup
        self.login_page = LoginPage(self.driver)
        self.product_list_page = ProductListPage(self.driver)
        self.edit_product_page = EditProductPage(self.driver)
        self.driver.get(self.login_page.url)
        self.logger.info("Launching application")
        self.driver.maximize_window()
        self.logger.info("Providing customer details for login")
        self.login_page.set_email(self.admin_email)
        self.login_page.set_password(self.admin_password)
        self.login_page.click_signin()
        sleep(3)
        self.driver.get(self.base_url)

    def test_create_new_product(self, setup, preconditions):
        self.product_list_page.click_create_product_btn()

        self.edit_product_page.get_name_input().clear()
        self.edit_product_page.set_name(self.product_name)

        self.edit_product_page.get_price_input().clear()
        self.edit_product_page.set_price(self.price)

        self.edit_product_page.get_brand_input().clear()
        self.edit_product_page.set_brand(self.brand)

        self.edit_product_page.get_stock_input().clear()
        self.edit_product_page.set_stock(self.quantity)

        self.edit_product_page.get_category_input().clear()
        self.edit_product_page.set_category(self.category)

        self.edit_product_page.get_description_input().clear()
        self.edit_product_page.set_description(self.description)

        actions = ActionChains(self.driver)
        actions.move_to_element(self.edit_product_page.get_update_btn()).perform()
        sleep(2)
        self.edit_product_page.click_update_btn()
        sleep(3)

        assert self.driver.current_url == 'http://127.0.0.1:8000/#/admin/productlist'