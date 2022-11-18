import asyncio
import csv
import os
from aiohttp import ClientSession

from aioscrape.daraz import get_products
from aioscrape.utils import parse_quantities, request, write_to_csv


async def scrape(url, session, products_file):
    print('Scraping...')
    task = asyncio.create_task(request(url, session))
    task.idx = url

    done, _ = await asyncio.wait([task])
    results = {}
    exceptions = {}
    for task in done:
        exc = task.exception()
        if exc:
            exceptions[task.idx] = exc
        else:
            resp = task.result()
            data = await resp.json()
            results[task.idx] = data

    products = get_products(results[url])
    write_to_csv(products_file, products, fieldnames=['name'])


def process(input_file, output_file='aioscrape/csv/quantities.csv'):
    print('Processing...')
    with open(input_file) as file:
        reader = csv.reader(file)
        next(reader, None)
        new_rows = []
        for row in reader:
            quantities = parse_quantities(row[0])
            if not quantities:
                new_rows.append({
                    'name': row[0],
                    'amount': None,
                    'unit': None
                })
            else:
                for q in quantities:
                    new_rows.append({
                        'name': row[0],
                        'amount': q[0],
                        'unit': q[1]
                    })
    write_to_csv(output_file, new_rows, fieldnames=['name', 'amount', 'unit']) 


async def start(term):
    url = f'https://www.daraz.com.np/catalog/?q={term}&ajax=true'
    products_file = f'aioscrape/csv/{term}.csv'
    
    async with ClientSession() as session:
        if not f'{term}.csv' in os.listdir('aioscrape/csv'):
            await scrape(url, session, products_file)    

    output_file = f'aioscrape/csv/{term}_quantities.csv'
    process(input_file=products_file, output_file=output_file)


if __name__ == '__main__':
    asyncio.run(start('daal'))