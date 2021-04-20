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


if __name__ == '__main__':
    pass
