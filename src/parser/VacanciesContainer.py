from src.parser.Vacancy import Vacancy
from src.parser.FirstJobEvent import FirstJobEvent
from typing import Union


class VacanciesContainer:
    def __init__(self):
        self._vacancies: list[Union[Vacancy, FirstJobEvent]] = []
        self._vacancies_counter = 0

    # adds 1 vacancy
    def add_vacancy(self, vacancy: Union[Vacancy, FirstJobEvent]) -> None:
        self._vacancies.append(vacancy)

    # adds multiple vacancies
    def add_vacancies(self, vacancies: list[Union[Vacancy, FirstJobEvent]]) -> None:
        self._vacancies.extend(vacancies)

    # returns only 1 vacancy or
    # None if you reached limit in forward or reverse direction, or if there are no vacs in self._vacancies

    # param following responses for direction which you want to go through the vacs list
    # if value None specified - func will return current vac (index counter doesn't change)
    # if value is True and False for following and previous, respectively (ind. counter changes higher and lower resp.)
    def get_vacancy(self, following: Union[bool, None] = None) -> Union[Vacancy, FirstJobEvent, None]:
        if len(self._vacancies) < 1:
            return None

        match following:
            case None:
                vacancy = self._vacancies[self._vacancies_counter]
                return vacancy
            case True:
                # Checking that the index doesn't become more than there are vacancies (than max index in vacs list)
                if (self._vacancies_counter + 1) < len(self._vacancies):
                    self._vacancies_counter += 1
                    vacancy = self._vacancies[self._vacancies_counter]
                    return vacancy
                else:
                    return None
            case False:
                # Checking that the index doesn't become less than 0
                # (we can't go backwards beyond first vacancy)
                if not ((self._vacancies_counter - 1) < 0):
                    self._vacancies_counter -= 1
                    vacancy = self._vacancies[self._vacancies_counter]
                    return vacancy
                else:
                    return None

    # it`s get_vacancy wrapper. Returns complete message with formatted data to send it via telegram bot to user
    def get_formatted_vacancy_msg(self, following=None) -> Union[str, None]:
        vacancy = self.get_vacancy(following=following)

        if vacancy:
            msg = f'{vacancy.title}\n\nКомпанія: {vacancy.company}\n\n{vacancy.short_info}\n' \
                           f'\n{vacancy.weblink}'

            return msg
        else:
            return None

    def refresh_counter(self) -> None:
        self._vacancies_counter = 0
        return None

    def clear(self):
        self._vacancies = []

