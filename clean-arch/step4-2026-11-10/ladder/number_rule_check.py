"""The ladder step's number rule, checked at $0 (DESIGN.md §5.3, check 4).

The rule: a bound, or a reference's value, is any finite number. It is kept as the exact decimal the model wrote, which is what
the checks compare and what the rung's text is written from. The float stored in production's `rungs` table is the nearest float,
a copy no reader on this path uses.
Claim under test: the written text of every accepted number reads back to the number, whatever its size, digits or spelling.
Run: python3 clean-arch/step4-2026-11-10/ladder/number_rule_check.py
"""
import json
import math
import random
from decimal import Decimal, InvalidOperation

OUTSIDE_THE_SET = 'not a finite number'      # what NaN, Infinity or a token the decimal type cannot hold is read as


def read_number_token(token_text):
    """The exact decimal a JSON number token writes, whatever its spelling. The decimal type holds any length of digits; it
    refuses only an exponent beyond about 10**18, which is read as OUTSIDE_THE_SET."""
    try:
        return Decimal(token_text)
    except InvalidOperation:
        return OUTSIDE_THE_SET


def parse_exactly(answer_text):
    """Parse the model's own text so every number is the exact decimal it wrote; no number token can make this raise."""
    return json.loads(answer_text, parse_float=read_number_token, parse_int=read_number_token,
                      parse_constant=lambda name: OUTSIDE_THE_SET)


def is_accepted(number):
    """Any finite number whose nearest float is finite too, so that production's table can hold its copy."""
    return isinstance(number, Decimal) and number.is_finite() and math.isfinite(float(number))


def written_text(number):
    """The text a rung shows: plain notation, no exponent, no trailing zeros, thousands separators on a whole number of 1,000 or
    more in size."""
    if number == 0:
        return '0'
    plain = format(number, 'f')
    if '.' in plain:
        plain = plain.rstrip('0').rstrip('.')
    if '.' not in plain:
        digits = plain.lstrip('-')
        grouped = f'{int(digits):,}' if len(digits) > 3 else digits
        return ('-' if plain.startswith('-') else '') + grouped
    return plain


def main():
    random.seed(20261110)
    numbers_checked = 0
    numbers_changed = 0
    for _ in range(400000):
        digit_count = random.randint(1, 30)
        mantissa = random.randint(1, 10 ** digit_count - 1)
        exponent = random.randint(-40, 40)
        number = Decimal(mantissa).scaleb(exponent) * random.choice((1, -1))
        if not is_accepted(number):
            continue
        numbers_checked += 1
        if Decimal(written_text(number).replace(',', '')) != number:
            numbers_changed += 1
    print('accepted numbers checked:', numbers_checked, '| changed by the written text:', numbers_changed)
    accepted_examples = ['0', '-0', '73.50', '119000000000', '999999999999999000', '0.5', '-250', '1234.5', '9007199254740993',
                         '2.5e18', '17234567891234567.89', '1e+0000', '1.0000000000000000000000000000000', '1e-400']
    refused_examples = ['1e400', 'NaN', 'Infinity', '-Infinity', '1e999999999999999999999999', '1e-999999999999999999999999']
    wrong = []
    for answer_text in accepted_examples + refused_examples:
        number = parse_exactly(answer_text)
        accepted = is_accepted(number)
        outcome = 'accepted, written ' + written_text(number)[:60] if accepted else 'refused'
        print(f'{answer_text[:40]:>40}  {outcome}')
        if accepted != (answer_text in accepted_examples):
            wrong.append(answer_text)
    if wrong:
        print('not as the rule says:', wrong)
    if numbers_checked == 0 or numbers_changed or wrong:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
