__version__ = '0.1.0'

from re import IGNORECASE, compile
from typing import Dict, List

_integers = (1000, 500, 100, 50, 10, 5, 1)
_literals = ('m', 'd', 'c', 'l', 'x', 'v', 'i')

_regex: str = r'^(m{0,4})(d?c{0,3}|c[dm])(l?x{0,3}|x[lc])(v?i{0,3}|i[vx])$'


_from_roman_numbers: Dict[str, int] = {
    char: num for char, num in zip(_literals, _integers)}
_to_roman_numbers: Dict[int, str] = {
    num: char for char, num in zip(_literals, _integers)}


def arabic_to_roman(number: int) -> str:
    """Convert arabic number to roman

    Args:
        number (int): Arabic number (0 < number < 5000)

    Raises:
        ValueError: Raises when number greater then 5000 or less then 1

    Returns:
        str: Converted number in lower case
    """
    if number in _to_roman_numbers:
        return _to_roman_numbers[number]

    if not (0 < number < 5000):
        raise ValueError('Number must be greater then 0 and less then 5000')

    bits: List[int] = [int(item) for item in str(number)]

    processed_bit: List[str] = [process_bit(item) for item in bits]

    result: List[str] = [process_roman_bit(processed_bit[i], len(
        processed_bit)-i) for i in range(len(processed_bit))]

    return ''.join(result)


def process_bit(bit: int) -> str:
    """Translate bit of arabic number to V and I query

    Args:
        bit (int): Arabic numbers

    Returns:
        str: Roman bit specific to the number
    """
    if bit == 0:
        return ''

    if bit in _to_roman_numbers:
        return _to_roman_numbers[bit]

    number: List[int] = [item for item in _integers if item - bit == 1]

    if len(number) != 0:
        return f'i{_to_roman_numbers[number[0]]}'

    result: str = ''
    for item in _integers:
        if bit == 0:
            break

        while bit >= item:
            result += _to_roman_numbers[item]
            bit -= item

    return result


def process_roman_bit(roman_bit: str, position: int) -> str:
    """Restruct roman bits relative to their position

    Args:
        roman_bit (str): Query of roman numbers to 1 arabic bit
        position (int): Position of the bit in arabi number

    Returns:
        str: Translated V and I to other positions
    """
    if position == 4:
        return ''.join('m' for _ in range(roman_to_arabic(roman_bit)))

    numbers: List[int] = [_from_roman_numbers[item] for item in roman_bit]
    powered_numbers: List[str] = [
        _to_roman_numbers[item*(10**(position-1))] for item in numbers]

    return ''.join(powered_numbers)


def roman_to_arabic(string: str) -> int:
    """Convert roman numbers to arabic

    Args:
        string (str): String that contains only roman numbers in any case

    Raises:
        ValueError: When string is empty
        ValueError: When string contains inappropriate chars

    Returns:
        int: Converted number
    """
    if string == '':
        raise ValueError('Empty input string')

    if not compile(_regex, IGNORECASE).search(string):
        raise ValueError('Inappropriate values')

    ints: List[int] = [_from_roman_numbers[item] for item in string.lower()]

    result: int = ints[-1]

    for i in range(len(ints)-1, 0, -1):
        result += (1 if ints[i-1] >= ints[i] else -1) * ints[i-1]

    return result


__all__ = [arabic_to_roman, roman_to_arabic, _regex]


def to_test(roman: str) -> str:
    converted_roman: int = roman_to_arabic(roman)
    converted_arabic: str = arabic_to_roman(converted_roman)

    return converted_arabic


if __name__ == '__main__':
    input_str: str = input('Roman or arabic number: ')

    try:
        out = roman_to_arabic(input_str) if compile(_regex).search(
            input_str) else arabic_to_roman(int(input_str))
    except ValueError as ve:
        print(ve)
    else:
        print(out)
