from pprint import pprint

import requests


class HeadHunterParser:
    AREA_MAPPING = {
        'Москва': 1,
    }

    def __init__(self, api_url):
        self.api_url = api_url

    def get_vacancies(self, text, area):
        url = f'{self.api_url}/vacancies'
        params = {
            'text': text,
            'area': HeadHunterParser.AREA_MAPPING[area],
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()


class HeadHunterVacancy:
    def __init__(self, vacancy):
        self.vacancy = vacancy

    def predict_rub_salary(self, from_coeff=1.2, to_coeff=0.8, rub_currency='RUR'):
        salary = self.vacancy['salary']

        if not salary or salary['currency'] != rub_currency:
            return None

        if not salary['from']:
            return salary['to'] * to_coeff

        if not salary['to']:
            return salary['from'] * from_coeff

        return (salary['from'] + salary['to']) / 2


def main():
    hh_parser = HeadHunterParser('https://api.hh.ru')

    user_area = 'Москва'
    search_text_template = 'программист {}'

    search_text = search_text_template.format('Python')

    vacancies = hh_parser.get_vacancies(search_text, user_area)

    hh_vacancies = []
    for vacancy in vacancies['items']:
        hh_vacancies.append(HeadHunterVacancy(vacancy))

    for hh_vacancy in hh_vacancies:
        print(hh_vacancy.predict_rub_salary())




    # top_languages = (
    #     'JavaScript',
    #     'Python',
    #     'Java',
    #     'TypeScript',
    #     'C#',
    #     'PHP',
    #     'C++',
    #     'C',
    #     'Shell',
    #     'Ruby',
    # )

    # top_languages_vacancies_amount = dict.fromkeys(top_languages)

    # for language in top_languages_vacancies_amount:
    #     search_text = search_text_template.format(language)
    #
    #     vacancies_amount = hh_parser.get_vacancies(search_text, user_area)['found']
    #
    #     top_languages_vacancies_amount[language] = vacancies_amount
    #
    # pprint(top_languages_vacancies_amount)



if __name__ == '__main__':
    main()
