#!/usr/bin/env python3
import json, sys
from beem import Steem
from beem.account import Account
from beemgraphenebase.account import PrivateKey, PublicKey 
from argparse import ArgumentParser
from beem.instance import set_shared_steem_instance

stmf = Steem(node=["https://apidev.blkcc.xyz"], custom_chains={"PULSAR":
    {'chain_assets': [{'asset': '@@000000013', 'id': 0, 'precision': 3, 'symbol': 'EUR'},
                      {'asset': '@@000000021', 'id': 1, 'precision': 3, 'symbol': 'PULSE'},
                      {'asset': '@@000000037', 'id': 2, 'precision': 6, 'symbol': 'VESTS'}],
     'chain_id': '07c687c01f134adaf217a9b9367d1cef679c3c020167fdd25ee8c403f687528e',
     'min_version': '0.101.0',
     'prefix': 'EUR'}
    }
)

def checkacc(username):
    try:
        acc = Account(username, steem_instance=stmf)
    except Exception as exception:
        assert type(exception).__name__ == 'AccountDoesNotExistsException'
        assert exception.__class__.__name__ == 'AccountDoesNotExistsException'
        return False
    else:
        return True

parser = ArgumentParser()
parser.add_argument('account', help="Name of the Pulsar account", type=str, nargs=1)
parser.add_argument('--all', help="If used, all information regarding the account will be displayed", action='store_true')
args = parser.parse_args()

if checkacc(args.account[0]):

    acc = Account(args.account[0], steem_instance=stmf)

    if args.all:
        print(json.dumps(acc.json(), indent=4))
    else:
        print(json.dumps(acc.profile, indent=4))

else:
    sys.exit("The account provided is not a valid account in the Pulsar Blockchain. Wrong account " + args.account[0])

# vim: set filetype=sh ts=4 sw=4 tw=0 wrap et:
