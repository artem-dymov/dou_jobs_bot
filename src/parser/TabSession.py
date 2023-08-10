from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options

from src.parser.Vacancy import Vacancy
from src.parser.VacanciesContainer import VacanciesContainer
from src.parser.FirstJobEvent import FirstJobEvent
from src.parser.FJEsContainer import FJEsContainer

from src.main import user_agent
from src.main import remote_chromedriver_link


class TabSession:
    website_link = 'https://jobs.dou.ua/vacancies/?'

    def __init__(self):
        options = Options()
        options.add_argument(user_agent)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # options.add_argument("start-maximized")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')

        options.headless = True
        # options.add_argument('--headless=')

        self.driver = webdriver.Remote(remote_chromedriver_link, options=options)
        self.driver.maximize_window()
        print(self.driver.page_source)

        self.open_homepage()

    def open_homepage(self):
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
        exps_raw = self.driver.find_elements(By.XPATH, '//div[@class="b-region-filter"]/ul[1]/li/a[not(@class="cl")]')

        # Experiences on html page saved like <a> tags, so we will save text of <a> tags
        # and click this links later
        exps = []
        for exp in exps_raw:
            exps.append(exp.text)
        return exps

    def get_cities(self) -> list[str]:
        cities_raw = self.driver.find_elements(By.XPATH, '//div[@class="b-region-filter"]/ul[2]/li/a[not(@class="cl")]')

        cities = []
        for city in cities_raw:
            cities.append(city.text)
        return cities

    def set_category(self, category_value) -> bool:
        try:
            self.driver.find_element(By.XPATH, f'//select[@name="category"]/option[@value="{category_value}"]').click()
            return True
        except Exception as e:
            print(e)
            return False

    def set_exp(self, exp_text) -> bool:
        try:
            self.driver.find_element(By.XPATH,
                                     f'//div[@class="b-region-filter"]/ul[1]/li/a[text()="{exp_text}"]').click()
            return True
        except Exception as e:
            print(e)
            return False

    def set_city(self, city_text) -> bool:
        try:
            self.driver.find_element(By.XPATH,
                                     f'//div[@class="b-region-filter"]/ul[2]/li/a[text()="{city_text}"]').click()
            return True
        except Exception as e:
            print(e)
            return False

    # this method loads all vacancies on webpage.
    # main target for this method is to click all "more" buttons, so you can have all vacancies on page
    def load_vacancies(self) -> None:
        while True:

            # New WebElement variable will be created when button
            # will be loaded after previous usage

            # Sometimes a button 'More 'may not have enough time to load properly before the driver
            # tries to click on it.
            # This try block prevents such exceptions.
            # Possible exception - ElementNotInteractableException.
            # Another possible exception is ElementClickInterceptedException,
            try:
                more_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="more-btn"]/a'))
                )

                # This method can be called without assigning its result to a variable,
                # but I made it to avoid PyCharm warnings (no effect code)
                loc = more_btn.location_once_scrolled_into_view

                more_btn.click()
            except exceptions.NoSuchElementException:
                break
            except exceptions.ElementNotInteractableException:
                break
            except exceptions.ElementClickInterceptedException:
                break
            except exceptions.TimeoutException:
                return None

    # downloads vacancies from webpage
    def download_vacancies(self) -> VacanciesContainer:

        # loading vacancies on webpage
        self.load_vacancies()

        # this list contains all vacancies in div tags
        vacancies_divs: list[WebElement] = self.driver.find_elements(By.XPATH, '//div[@class="vacancy"]')

        vacancies_container = VacanciesContainer()

        for vacancy_div in vacancies_divs:

            # this tag contains weblink to vac in href property and vac name in tag text
            a_tag: WebElement = vacancy_div.find_element(By.XPATH, './/div[@class="title"]/a')

            title: str = a_tag.text
            vac_link: str = a_tag.get_attribute('href')

            try:
                city = vacancy_div.find_element(By.XPATH, './/div[@class="title"]/span').text
            except Exception:
                city = 'не вказана'

            company: str = vacancy_div.find_element(By.XPATH, './/a[@class="company"]').text
            short_info: str = vacancy_div.find_element(By.XPATH, './/div[@class="sh-info"]').text

            vacancy = Vacancy(title, company, city, short_info, vac_link)
            vacancies_container.add_vacancy(vacancy)

        return vacancies_container

    # sends request text to search field on website and clicks submit
    def send_request(self, text: str) -> None:
        input_field: WebElement = self.driver.find_element(By.XPATH, '//input[@class="job"][@name="search"]')

        input_field.send_keys(text)
        input_field.submit()

    # Downloads first job events
    # Returns VacanciesContainer with FirstJobEvent objects inside it
    def download_fjes(self) -> FJEsContainer:
        fje_articles: list[WebElement] = self.driver.find_elements(By.XPATH,
                                                                     '//div[@class="first-job-events"]//article')

        fje_container = FJEsContainer()
        for fje_article in fje_articles:
            title = fje_article.find_element(By.XPATH, './/h2').text

            where_and_when: WebElement = fje_article.find_element(By.XPATH, './/div[@class="when-and-where"]')
            when = where_and_when.find_element(By.XPATH, './span').text

            # excluding "when" text from "where_and_when" element
            where = where_and_when.text.replace(when, '')

            short_info = fje_article.find_element(By.XPATH, './/p').text
            weblink = fje_article.find_element(By.XPATH, './/h2/a').get_attribute('href')

            fje = FirstJobEvent(title, where, when, short_info, weblink)
            fje_container.add_vacancy(fje)

        return fje_container



