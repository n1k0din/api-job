class LanguageStats:
    search_text_template = 'программист {}'

    def __init__(self, language, area, parser):
        self.language = language
        self.area = area
        self.parser = parser
        self.vacancies_found = 0
        self.vacancies_processed = 0
        self.average_salary = 0

    def get_all_vacancies(self):
        search_text = LanguageStats.search_text_template.format(self.language)
        vacancies_found, vacancies = self.parser.get_vacancies(search_text, self.area)

        self.vacancies_found = vacancies_found

        return vacancies

    def calc_language_stats(self):
        vacancies = self.get_all_vacancies()

        predicted_salaries = []
        for vacancy in vacancies:
            predicted_salary = self.parser.predict_rub_salary(vacancy)
            if predicted_salary:
                predicted_salaries.append(int(predicted_salary))

        self.vacancies_processed = len(predicted_salaries)

        self.average_salary = int(
            sum(predicted_salaries) / self.vacancies_processed
        )

    def build_stats_dict(self):
        return {
            self.language: {
                'vacancies_found': self.vacancies_found,
                'vacancies_processed': self.vacancies_processed,
                'average_salary': self.average_salary,
            }
        }


if __name__ == '__main__':
    pass
