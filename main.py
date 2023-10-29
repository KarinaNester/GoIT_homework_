import argparse
import sys
from datetime import datetime, timedelta

import httpx
import asyncio
import platform


class HttpError(Exception):
    pass


async def request(url: str):
    async with httpx.AsyncClient() as client:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, timeout=10)  # Задаємо таймаут на 10 секунд
                if r.status_code == 200:
                    result = r.json()
                    return result
                else:
                    raise HttpError(f"Error status: {r.status_code} for {url}")
        except httpx.ReadTimeout:
            raise HttpError("Timeout occurred while fetching data.")


async def get_currency_rates(num_days):
    currency_rates = []
    today = datetime.now()

    for i in range(num_days):
        current_date = today - timedelta(days=i)
        shift = current_date.strftime("%d.%m.%Y")
        data = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={shift}')

        if 'exchangeRate' in data:
            rates = {}
            for rate in data['exchangeRate']:
                if rate['currency'] in ['EUR', 'USD']:
                    rates[rate['currency']] = {
                        'sale': float(rate['saleRate']),
                        'purchase': float(rate['purchaseRate'])
                    }
            currency_rates.append({shift: rates})

    return currency_rates


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    parser = argparse.ArgumentParser()
    parser.add_argument('num_days', type=int, help='Number of days ago to retrieve currency rates')
    args = parser.parse_args()

    if args.num_days > 10:
        print("Error: You can retrieve currency rates for up to the last 10 days.")
    else:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(get_currency_rates(args.num_days))
        print(result)
