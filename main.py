import os
from collections import defaultdict
from functools import partial
from itertools import count

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable

HH_MOSCOW_ID = 1
SJ_MOSCOW_ID = 4
SJ_SOFTWARE_DEVELOP_SECTION_ID = 48

SEARCH_TEMPLATE = 'программист {}'


def get_hh_language_vacancies(
    language,
    area_id,
    api_url='https://api.hh.ru',
    per_page=20,
    max_results=2000
):
    search_text = SEARCH_TEMPLATE.format(language)

    url = f'{api_url}/vacancies'
    params = {
        'text': search_text,
        'area': area_id,
        'page': 0,
        'per_page': per_page,
    }

    vacancies = []
    for page in count():
        params['page'] = page

        response = requests.get(url, params=params)
        response.raise_for_status()

        page_data = response.json()

        vacancies.extend(page_data['items'])

        if page >= page_data['pages'] \
                or page * per_page >= max_results - per_page:
            break

    return {'total': page_data['found'], 'items': vacancies}


def get_sj_language_vacancies(
    language,
    area_id,
    api_key,
    api_url='https://api.superjob.ru/2.20/',
    per_page=20,
    max_results=500
):
    search_text = SEARCH_TEMPLATE.format(language)

    url = f'{api_url}/vacancies'
    params = {
        'keyword': search_text,
        'town': area_id,
        'catalogues[]': SJ_SOFTWARE_DEVELOP_SECTION_ID,
        'page': 0,
        'count': per_page,
    }

    headers = {'X-Api-App-Id': api_key}

    vacancies = []
    for page in count():
        params['page'] = page

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        page_data = response.json()

        vacancies.extend(page_data['objects'])

        if not page_data['more'] \
                or page * per_page >= max_results - per_page:
            break

    return {'total': page_data['total'], 'items': vacancies}


def predict_hh_rub_salary(hh_vacancy, rub_currency='RUR'):
    salary = hh_vacancy['salary']

    if not salary or salary['currency'] != rub_currency:
        return None

    return predict_salary(salary['from'], salary['to'])


def predict_sj_rub_salary(sj_vacancy, rub_currency='rub'):
    payment_from, payment_to = sj_vacancy['payment_from'], sj_vacancy['payment_to']

    if not (payment_from or payment_to) \
            or sj_vacancy['currency'] != rub_currency:
        return None

    return predict_salary(payment_from, payment_to)


def calc_language_stats(vacancies, salary_predictor):
    predicted_salaries = []
    for vacancy in vacancies['items']:
        predicted_salary = salary_predictor(vacancy)
        if predicted_salary:
            predicted_salaries.append(int(predicted_salary))

    vacancies_processed = len(predicted_salaries)

    average_salary = int(
        sum(predicted_salaries) / vacancies_processed
    )

    return {
        'vacancies_found': vacancies['total'],
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary,
    }


def predict_salary(salary_from, salary_to, from_coeff=1.2, to_coeff=0.8):
    if not salary_from:
        return salary_to * to_coeff

    if not salary_to:
        return salary_from * from_coeff

    return (salary_from + salary_to) / 2


def build_lang_stats_table(title, lang_stats):
    table_header = ('Язык', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зп')
    table_data = [table_header]

    for lang, stats in lang_stats.items():
        table_data.append(
            (
                lang,
                stats['vacancies_found'],
                stats['vacancies_processed'],
                stats['average_salary'],
            )
        )

    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table


def main():
    load_dotenv('.env')
    sj_api_key = os.getenv('SJ_KEY')

    top_languages = (
        'JavaScript',
        'Python',
        'Java',
        'TypeScript',
        'C#',
        'PHP',
        'C++',
        'C',
        'Shell',
        'Ruby',
    )

    lang_stats = defaultdict(dict)

    job_portal_parameters = {
        'HeadHunter Moscow': {
            'predictor': predict_hh_rub_salary,
            'vacancies_getter': get_hh_language_vacancies,
            'area_id': HH_MOSCOW_ID,
        },
        'SuperJob Moscow': {
            'predictor': predict_sj_rub_salary,
            'vacancies_getter': partial(get_sj_language_vacancies, api_key=sj_api_key),
            'area_id': SJ_MOSCOW_ID,
        },

    }

    for job_portal, params in job_portal_parameters.items():
        for language in top_languages:
            vacancies = params['vacancies_getter'](
                language,
                area_id=params['area_id'],
                max_results=60
            )
            lang_stats[job_portal][language] = calc_language_stats(vacancies, params['predictor'])
        print(build_lang_stats_table(job_portal, lang_stats[job_portal]))


if __name__ == '__main__':
    main()
