from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class TabSession:
    website_link = 'https://jobs.dou.ua'

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.website_link)

    # method parse available categories from website
    def get_categories(self) -> list[str]:
        categories_raw = self.driver.find_elements(By.XPATH, '//select[@name="category"]/option[not(@value="")]')

        # Creating new list for values from tag objects from Selenium
        categories = []
        for category in categories_raw:
            categories.append(category.get_property('value'))
        return categories

    # exp - experience
    def get_exps(self) -> list[str]:
        exps_raw = self.driver.find_elements(By.XPATH, '//div[@class="b-region-filter"]/ul[1]/li/a')

        # Experiences on html page saved like <a> tags, so we will save text of <a> tags
        # and click this links later
        exps = []
        for exp in exps_raw:
            exps.append(exp.text)
        return exps

    def get_city(self) -> list[str]:
        cities_raw = self.driver.find_elements(By.XPATH, '//div[@class="b-region-filter"]/ul[2]/li/a')

        cities = []
        for city in cities_raw:
            cities.append(city.text)
        return cities


