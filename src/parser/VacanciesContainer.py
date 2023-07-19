from Vacancy import Vacancy
from typing import Union


class VacanciesContainer:
    def __init__(self):
        self._vacancies = []
        self._vacancies_counter = 0

    # adds 1 vacancy
    def add_vacancy(self, vacancy: Vacancy) -> None:
        self._vacancies.append(vacancy)

    # adds multiple vacancies
    def add_vacancies(self, vacancies: list[Vacancy]) -> None:
        self._vacancies.extend(vacancies)

    # method get_vacancies returns not all vacancies but some quantity of them
    # Important! this method returns always new vacancies if container have them
    # You can refresh counter to go through list of vacancies again
    def get_vacancies(self, quantity: int) -> Union[list[Vacancy], None]:
        vacancies = []
        for i in range(quantity):
            if self._vacancies_counter < len(self._vacancies):
                vacancies.append(self._vacancies[self._vacancies_counter])
                self._vacancies_counter += 1

        if len(vacancies) > 0:
            return vacancies
        else:
            return None

    def refresh_counter(self) -> None:
        self._vacancies_counter = 0
        return None

    def clear(self):
        self._vacancies = []
