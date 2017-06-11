#!/usr/bin/env python

"""randogen.py
"""

import json
import random

import requests
from Crypto.PublicKey import RSA

class RandoGen(object):
    """Class to have Fun with random.org; includes random number and
    RSA keypair generators.
    """

    # including this here in the interest of time; never commit API keys for real code!
    API_KEY = '701b81d1-3151-4c31-b036-f30449c0f176'

    def fetch_randos(self, num_randos, min_rando=0, max_rando=255, replace='True', base=10, return_bytes=True):
        if num_randos <= 0:
            if return_bytes:
                return bytearray([])
            else:
                return []
        data = {'jsonrpc':'2.0',
                'method': 'generateIntegers',
                'params': { 'apiKey': self.API_KEY,
                            'n': num_randos,
                            'min': min_rando,
                            'max': max_rando,
                            'replacement': replace,
                            'base': base },
                'id': random.randrange(0, 10000) }

        r = requests.post('https://api.random.org/json-rpc/1/invoke', headers={'content-type': 'application/json'}, data=json.dumps(data))
        randos = r.json()['result']['random']['data']
        if return_bytes:
            return bytearray(randos)
        else:
            return randos

    def generate_keypair(self, privatepath, publicpath):
        random_generator = self.fetch_randos
        private_key = RSA.generate(2048, random_generator)
        public_key = private_key.publickey()
        with open(privatepath, 'wb') as priv, open(publicpath, 'wb') as pub:
            priv.write(private_key.exportKey())
            pub.write(public_key.exportKey())

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='''
    Welcome to randogen.py help! This module will help you interact with random.org.
    There are two main commands:
        python randogen.py -r
        python randogen.py -k
    The -r option generates and prints random integers from random.org to stdout.
    The -k option uses random integers from random.org to create an RSA keypair.

    There are several options for each command, so be sure to check the help with:
        python randogen.py -h
        ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-k', '--keypair', action='store_true',
                        help='generate and save an RSA keypair')
    parser.add_argument('--publicpath',
                        default='./id_rsa.pub',
                        help='path for generated public key')
    parser.add_argument('--privatepath',
                        default='./id_rsa',
                        help='path for generated private key')

    parser.add_argument('-r', '--randos', action='store_true',
                        help='generate and print random numbers from random.org')
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

    r = RandoGen()
    if args.keypair and args.randos:
        print('Please specify "--keypair" or "--randos". Type `python randogen.py -h` for help')
    elif not args.keypair and not args.randos:
        print('Please specify "--keypair" or "--randos". Type `python randogen.py -h` for help')
    elif args.keypair:
        key = r.generate_keypair(args.privatepath, args.publicpath)
    elif args.randos:
        print(r.fetch_randos(args.num, args.min, args.max, args.noreplacement, args.base, return_bytes=False))
