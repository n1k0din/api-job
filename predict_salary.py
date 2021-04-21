def predict_salary(salary_from, salary_to, from_coeff=1.2, to_coeff=0.8):
    if not salary_from:
        return salary_to * to_coeff

    if not salary_to:
        return salary_from * from_coeff

    return (salary_from + salary_to) / 2


if __name__ == '__main__':
    pass
