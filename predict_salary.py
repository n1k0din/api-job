def predict_salary(salary_from, salary_to, from_coeff=1.2, to_coeff=0.8):
    if not salary_from:
        return salary_to * to_coeff

    if not salary_to:
        return salary_from * from_coeff

    return (salary_from + salary_to) / 2


def predict_rub_salary_hh(hh_vacancy, rub_currency='RUR'):
    salary = hh_vacancy['salary']

    if not salary or salary['currency'] != rub_currency:
        return None

    return predict_salary(salary['from'], salary['to'])


def predict_rub_salary_sj(sj_vacancy, rub_currency='rub'):
    payment_from, payment_to = sj_vacancy['payment_from'], sj_vacancy['payment_to']
    if not (payment_from or payment_to) \
            or sj_vacancy['currency'] != rub_currency:
        return None

    return predict_salary(payment_from, payment_to)


if __name__ == '__main__':
    pass
