#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

import jwt
import requests

import settings
from settings import TOKEN_EXPIRATION


class ExanteApi():
    token = (None, None)
    algo = 'HS256'

    def __init__(self, client_id, app_id, shared_key):
        self.client_id = client_id
        self.app_id = app_id
        self.shared_key = shared_key

    def get_token(self):
        now = datetime.now()

        if self.token[0]:
            if (now - self.token[1]).total_seconds() < TOKEN_EXPIRATION:
                return self.token[0]

        claims = {
            'iss': self.client_id,
            'sub': self.app_id,
            'aud': ['symbols', ],
            'iat': int(now.timestamp()),
            'exp': int(now.timestamp()) + TOKEN_EXPIRATION
        }

        new_token = str(
            jwt.encode(claims, self.shared_key, self.algo),
            'utf-8'
        )
        self.token = (new_token, now)

        return new_token

    def request(self, endpoint, params=None):
        token = self.get_token()
        result = requests.get(
            settings.API_URL + endpoint,
            headers={'Authorization': 'Bearer {0}'.format(token)},
            params=params
        )
        result.raise_for_status()
        return result.json()

    def get_stocks(self):
        stocks = self.request('/types/STOCK')
        return stocks


api = ExanteApi(
    client_id=settings.API_CLIENT_ID,
    app_id=settings.API_APP_ID,
    shared_key=settings.API_SHARED_KEY
)

stocks = api.get_stocks()

# structuring data
data = {}
for stock in stocks:
    country = stock.get('country', None)
    if country:
        stock_info = {
            stock['ticker']: stock,
        }
        if country in data:
            if stock['exchange'] in data[country]:
                data[country][stock['exchange']][stock['ticker']] = stock
            else:
                data[country][stock['exchange']] = {
                    stock['ticker']: stock,
                }
        else:
            data[country] = {
                stock['exchange']: {
                    stock['ticker']: stock,
                },
            }

# show stats for structured data
for country, exchanges in data.items():
    print(country)
    for exchange, stocks in exchanges.items():
        print('  {0} - {1}'.format(
            exchange,
            len(stocks.keys()),
        ))







