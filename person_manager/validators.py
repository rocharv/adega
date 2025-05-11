import re
from django.core.exceptions import ValidationError


def validate_cpf(cpf: str):
    # Remove non-digit characters from cpf string
    clean_cpf = re.sub(r"\D","", cpf)
    len_clean_cpf: int = len(clean_cpf)
    if len_clean_cpf > 11:
        raise ValidationError("CPF não pode ter mais de 11 dígitos.")
    clean_cpf: str = "0" * (11 - len_clean_cpf) + clean_cpf

    # Validate first check digit
    check_digit_1: int = 0
    digit_sum: int = 0
    for i in range(9):
        digit_sum += (10 - i) * int(clean_cpf[i])
    mod_digit_sum_11: int = digit_sum % 11
    if mod_digit_sum_11 > 2:
        check_digit_1 = 11 - mod_digit_sum_11
    else:
        check_digit_1 = 0
    if check_digit_1 != int(clean_cpf[9]):
        raise ValidationError(
            "CPF inválido: erro no primeiro dígito verificador."
        )
    clean_cpf += str(check_digit_1)

    # Validate second check digit
    check_digit_2: int = 0
    digit_sum = 0
    for i in range(10):
        digit_sum += (11 - i) * int(clean_cpf[i])
    mod_digit_sum_11 = digit_sum % 11
    if mod_digit_sum_11 > 2:
        check_digit_2 = 11 - mod_digit_sum_11
    else:
        check_digit_2 = 0
    if check_digit_2 != int(clean_cpf[10]):
        raise ValidationError(
            "CPF inválido: erro no segundo dígito verificador."
        )
