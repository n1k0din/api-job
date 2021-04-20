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


if __name__ == '__main__':
    pass
