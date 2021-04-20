from itertools import count

import requests


class HeadHunterParser:
    AREA_MAPPING = {
        'Москва': 1,
    }

    def __init__(self, api_url, per_page=20, max_results=2000):
        self.api_url = api_url
        self.per_page = per_page
        self.max_results = max_results

    def get_vacancies(self, text, area):
        url = f'{self.api_url}/vacancies'

        params = {
            'text': text,
            'area': HeadHunterParser.AREA_MAPPING[area],
            'page': 0,
            'per_page': self.per_page,
        }

        vacancies = []
        for page in count():
            params['page'] = page

            response = requests.get(url, params=params)
            response.raise_for_status()

            page_data = response.json()

            vacancies.extend(page_data['items'])

            if page >= page_data['pages'] \
                    or page * self.per_page >= self.max_results - self.per_page:
                break

        return page_data['found'], vacancies


if __name__ == '__main__':
    pass
