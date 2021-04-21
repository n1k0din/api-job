import os
from collections import defaultdict

from dotenv import load_dotenv
from terminaltables import AsciiTable

from headhunter_parser import HeadHunterParser
from language_stats import LanguageStats
from superjob_parser import SuperjobParser


def get_lang_stats(language, area, parser):
    stats = LanguageStats(language, area, parser)
    stats.calc_language_stats()
    return stats.build_stats_dict()


def print_lang_stats(title, lang_stats):
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
    print(table_instance.table)


def main():
    user_area = 'Москва'

    hh_parser = HeadHunterParser('https://api.hh.ru', max_results=2000)

    load_dotenv('.env')
    sj_api_key = os.getenv('SJ_KEY')
    sj_parser = SuperjobParser('https://api.superjob.ru/2.20/', sj_api_key, max_results=500)

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

    parsers = {
        'HeadHunter Moscow': hh_parser,
        'Superjob Moscow': sj_parser,
    }

    language_stats = defaultdict(dict)

    for language in top_languages:
        for title, parser in parsers.items():
            language_stats[title] |= get_lang_stats(language, user_area, parser)

    for title, language_stat in language_stats.items():
        print_lang_stats(title, language_stat)


if __name__ == '__main__':
    main()
