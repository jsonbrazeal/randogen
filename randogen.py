#!/usr/bin/env python

"""randogen.py
"""

import json
import random

import requests

API_KEY = None

def fetch_randos(num_randos, min_rando, max_rando, replace, base):
    data = {'jsonrpc':'2.0',
            'method': 'generateIntegers',
            'params': { 'apiKey': API_KEY,
                        'n': num_randos,
                        'min': min_rando,
                        'max': max_rando,
                        'replacement': replace,
                        'base': base },
            'id': random.randrange(0, 10000) }

    print('request:')
    print(data)
    r = requests.post('https://api.random.org/json-rpc/1/invoke', headers={'content-type': 'application/json'}, data=json.dumps(data))
    print('response:')
    print(r.json())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--num',
                        default=10,
                        type=int,
                        help='number of random integers to generate')
    parser.add_argument('--min',
                        default=0,
                        type=int,
                        help='minimum random integer to generate')
    parser.add_argument('--max',
                        default=10000,
                        type=int,
                        help='maximum random integer to generate')
    parser.add_argument('--base',
                        default=10,
                        type=int,
                        help='base of integers to generate')
    parser.add_argument('--noreplacement',
                        action='store_false',
                        default=True,
                        help='set to prevent generator from producing the same number more than once')
    args = parser.parse_args()

    fetch_randos(args.num, args.min, args.max, args.noreplacement, args.base)
