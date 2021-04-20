from pprint import pprint

import requests


class HeadHunterParser:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_vacancies_by_name(self, text):
        url = f'{self.api_url}/vacancies'
        params = {'text': text}

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()


def main():
    hh_parser = HeadHunterParser('https://api.hh.ru')
    pprint(hh_parser.get_vacancies('программист'))


if __name__ == '__main__':
    main()
