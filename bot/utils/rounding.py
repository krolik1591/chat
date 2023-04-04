from math import floor


def round_down(num, sign_after_comma):
    return floor(float(num) * 10**sign_after_comma) / 10**sign_after_comma
