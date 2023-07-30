from src.parser.Vacancy import Vacancy
from typing import Union


class VacanciesContainer:
    def __init__(self):
        self._vacancies: list[Vacancy] = []
        self._vacancies_counter = 0

    # adds 1 vacancy
    def add_vacancy(self, vacancy: Vacancy) -> None:
        self._vacancies.append(vacancy)

    # adds multiple vacancies
    def add_vacancies(self, vacancies: list[Vacancy]) -> None:
        self._vacancies.extend(vacancies)

    # method get_vacancies returns not all vacancies but some quantity of them
    # Important! By default, this method returns always new vacancies if container have them
    # You can refresh counter to go through list of vacancies again.
    # Or you can set parameter 'following' to 'False' to go backwards
    def get_vacancies(self, quantity: int, following=True) -> Union[list[Vacancy], None]:
        vacancies = []
        if self._vacancies is None:
            return None

        for i in range(quantity):
            if self._vacancies_counter < len(self._vacancies):
                vacancies.append(self._vacancies[self._vacancies_counter])
                self._vacancies_counter += 1
            else:
                return None
        if len(vacancies) > 0:
            return vacancies
        else:
            return None

    def refresh_counter(self) -> None:
        self._vacancies_counter = 0
        return None

    def clear(self):
        self._vacancies = []

