from string import ascii_lowercase
from django.utils.text import slugify

from datetime import datetime


def get_slug(url):
    return slugify(rus_to_eng(url)) + f'-{int(datetime.timestamp(datetime.today()))}'
def rus_to_eng(word):
    letters = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'j',
        'з': 'z',
        'и': 'i',
        'й': 'i',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 'c',
        'т': 't',
        'у': 'y',
        'ф': 'f',
        'х': 'х',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sj',
        'ъ': 'i',
        'ы': 'i',
        'ь': 'i',
        'э': 'э',
        'ю': 'u',
        'я': 'ia'

    }

    new_word = ''
    for i in word:
        if i.lower() in letters:
            new_word += letters[i.lower()]
        elif i.lower() in ('-', ' ', '_') or i.isdigit():
            new_word += i.lower()
        elif i.lower() in ascii_lowercase:
            new_word += i.lower()
        else:
            new_word += ''

    return new_word


