from select import select
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProductPage:
    url = "http://127.0.0.1:8000/#/product/6"
    add_to_cart_btn = '//*[@id="root"]/main/div/div/div/div[1]/div[3]/div/div/div[4]/button'
    select_rating_xpath = '//*[@id="rating"]'
    comment_input_xpath = '//*[@id="comment"]'
    submit_btn_xpath = '//*[@id="root"]/main/div/div/div/div[2]/div/div[2]/div/form/button'
    reviewed_message_xpath = '//*[@id="root"]/main/div/div/div/div[2]/div/div/div[3]/div'
    submit_btn = 'button[type="submit"].btn.btn-primary'


    def __init__(self, driver):
        self.driver = driver

    def get_select_dropdown_element(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.select_rating_xpath)))

    def get_comment_input(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.comment_input_xpath)))


    def select_rating_option(self, option):
        dropdown_element = self.get_select_dropdown_element()
        select = Select(dropdown_element)
        select.select_by_visible_text(option)

    def insert_comment(self, comment):
        input_field = self.get_comment_input()
        input_field.send_keys(comment)

    def click_on_submit_btn(self):
        self.driver.find_element(By.CSS_SELECTOR, self.submit_btn).click()

    def get_reviewed_msg(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.reviewed_message_xpath)))

    def get_rating(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 'i.fas.fa-star[style="color: rgb(248, 232, 37);"]')

    def click_on_add_to_cart(self):
        self.driver.find_element(By.XPATH, self.add_to_cart_btn).click()
