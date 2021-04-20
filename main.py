from pprint import pprint

from headhunter_parser import HeadHunterParser
from language_stats import LanguageStats


def main():
    user_area = 'Москва'

    hh_parser = HeadHunterParser('https://api.hh.ru', max_results=200)

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

    top_languages_stats = {}
    for language in top_languages:
        language_stats = LanguageStats(language, user_area, hh_parser)
        language_stats.calc_language_stats()
        top_languages_stats |= language_stats.build_stats_dict()

    pprint(top_languages_stats)


if __name__ == '__main__':
    main()
