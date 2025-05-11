import re
from django.core.exceptions import ValidationError


def validate_cnpj(cnpj: str):
    # Remove non-digit characters from cnpj string
    clean_cnpj = re.sub(r"\D","", cnpj)
    len_clean_cnpj: int = len(clean_cnpj)
    if len_clean_cnpj > 14:
        raise ValidationError("CNPJ não pode ter mais de 14 dígitos.")
    clean_cnpj: str = "0" * (14 - len_clean_cnpj) + clean_cnpj

    # Validate first check digit
    check_digit_1: int = 0
    digit_sum: int = 0
    for i in range(12):
        if i < 4:
            digit_sum += (5 - i) * int(clean_cnpj[i])
        else:
            digit_sum += (13 - i) * int(clean_cnpj[i])
    mod_digit_sum_11: int = digit_sum % 11
    if mod_digit_sum_11 > 1:
        check_digit_1 = 11 - mod_digit_sum_11
    else:
        check_digit_1 = 0
    if check_digit_1 != int(clean_cnpj[12]):
        raise ValidationError(
            "CNPJ inválido: erro no primeiro dígito verificador."
        )

    clean_cnpj += str(check_digit_1)

    # Validate second check digit
    check_digit_2: int = 0
    digit_sum: int = 0
    for i in range(13):
        if i < 5:
            digit_sum += (6 - i) * int(clean_cnpj[i])
        else:
            digit_sum += (14 - i) * int(clean_cnpj[i])
    mod_digit_sum_11: int = digit_sum % 11
    if mod_digit_sum_11 > 1:
        check_digit_2 = 11 - mod_digit_sum_11
    else:
        check_digit_2 = 0
    if check_digit_2 != int(clean_cnpj[13]):
        raise ValidationError(
            "CNPJ inválido: erro no segundo dígito verificador."
        )
