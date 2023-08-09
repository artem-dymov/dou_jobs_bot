from src.parser.VacanciesContainer import VacanciesContainer
from src.parser.FirstJobEvent import FirstJobEvent
from typing import Union


# Container for FirstJobEvent objects
class FJEsContainer(VacanciesContainer):
    def get_formatted_vacancy_msg(self, following=None) -> Union[str, None]:
        vacancy: FirstJobEvent = self.get_vacancy(following=following)

        if vacancy:
            msg = f'{vacancy.title}\n\nКоли і де: {vacancy.when}, {vacancy.where}\n\n{vacancy.short_info}' \
                  f'\n\n{vacancy.weblink}'

            return msg
        else:
            return None
