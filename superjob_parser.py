from itertools import count

import requests

from predict_salary import predict_salary


class SuperjobParser:
    AREA_MAPPING = {
        'Москва': 4,
    }

    SOFTWARE_DEVELOP_SECTION_ID = 48

    def __init__(self, api_url, api_key, rub_currency='rub', per_page=20, max_results=500):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {'X-Api-App-Id': api_key}
        self.rub_currency = rub_currency
        self.per_page = per_page
        self.max_results = max_results

    def get_vacancies(self, search_text, area):
        url = f'{self.api_url}/vacancies'

        params = {
            'keyword': search_text,
            'town': self.AREA_MAPPING[area],
            'catalogues[]': self.SOFTWARE_DEVELOP_SECTION_ID,
            'page': 0,
            'count': self.per_page,
        }

        vacancies = []
        for page in count():
            params['page'] = page

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            page_data = response.json()

            vacancies.extend(page_data['objects'])

            if not page_data['more'] \
                    or page * self.per_page >= self.max_results - self.per_page:
                break

        return page_data['total'], vacancies

    def predict_rub_salary(self, sj_vacancy):
        payment_from, payment_to = sj_vacancy['payment_from'], sj_vacancy['payment_to']
        if not (payment_from or payment_to) \
                or sj_vacancy['currency'] != self.rub_currency:
            return None

        return predict_salary(payment_from, payment_to)


if __name__ == '__main__':
    pass
