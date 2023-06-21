import json
import requests


class APIException(Exception):
    """Общий класс исключений для не корректного ввода данных"""
    pass


class Request:
    # метод обработки запроса и вызова исключений
    @staticmethod
    def get_price(base, quote, amount):
        r_update = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        curses = json.loads(r_update.content)
        base_up, quote_up = base.upper(), quote.upper()
        try:
            if base_up != 'RUB':
                base_curse = round(curses['Valute'][base_up]['Value'], 4)
        except KeyError:
            raise APIException(f'не правильно введен код начальной валюты: {base}')
        try:
            if quote_up != 'RUB':
                quote_curse = round(curses['Valute'][quote_up]['Value'], 4)
        except KeyError:
            raise APIException(f'не правильно введен код валюты перевода: {quote}')
        try:
            tested_amount = round(float(amount.replace(',', '.')), 4)
        except ValueError:
            raise APIException(f'не правильно введена сумма: {amount}')
        if tested_amount <= 0:
            raise APIException(f'сумма не может быть меньше или равна 0.')

        if base_up == quote_up:
            raise APIException('значения валют должны быть разные')
        elif base_up == 'RUB':
            return f'{Request.format(tested_amount)} {base_up} = ' \
                   f'{Request.format(tested_amount/quote_curse)} {quote_up}'
        elif quote_up == 'RUB':
            return f'{Request.format(tested_amount)} {base_up} = ' \
                   f'{Request.format(base_curse * tested_amount)} {quote_up}'
        elif base_up in curses['Valute'] and quote_up in curses['Valute']:
            return f'{Request.format(tested_amount)} {base_up} = ' \
                   f'{Request.format(base_curse * tested_amount / quote_curse)} {quote_up}'

    # метод форматирования числа
    @staticmethod
    def format(amount):
        return '{0:,}'.format(round(amount, 4)).replace(',', ' ')

    # метод получения словаря с краткой сводкой по валютам для использования телеботом
    @staticmethod
    def get_dict():
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        _values = json.loads(r.content)
        dict_values = dict()
        dict_values.setdefault('RUB', ['Российский рубль', 1, 1])
        for val in _values['Valute'].values():
            dict_values.setdefault(val['CharCode'], [val['Name'], val['Nominal'], val['Value']])
        return dict_values
