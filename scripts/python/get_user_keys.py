#!/usr/bin/env python3
from beem import Steem
from beem.account import Account
from beemgraphenebase.account import PasswordKey
from argparse import ArgumentParser
from beem.instance import set_shared_steem_instance
import json, sys

stm = Steem(node=["https://apidev.blkcc.xyz"], custom_chains={"PULSAR":
    {'chain_assets': [{'asset': '@@000000013', 'id': 0, 'precision': 3, 'symbol': 'EUR'},
                      {'asset': '@@000000021', 'id': 1, 'precision': 3, 'symbol': 'PULSE'},
                      {'asset': '@@000000037', 'id': 2, 'precision': 6, 'symbol': 'VESTS'}],
     'chain_id': '07c687c01f134adaf217a9b9367d1cef679c3c020167fdd25ee8c403f687528e',
     'min_version': '0.101.0',
     'prefix': 'EUR'}
    }
)

set_shared_steem_instance(stm)
prefix = stm.prefix

parser = ArgumentParser()
parser.add_argument('account', type=str, nargs=1)
parser.add_argument('password', type=str, nargs=1)
args = parser.parse_args()

while True:
    try:
        account = Account(args.account[0])
        break
    except Exception as exception:
        assert type(exception).__name__ == 'AccountDoesNotExistsException'
        assert exception.__class__.__name__ == 'AccountDoesNotExistsException'
        sys.exit("The account provided doesn't exist in the EFTG Blockchain. Wrong account " + args.account[0])

password = args.password[0]

key_auths_public = {}
key_auths_private = {}
blk_auths_public = {}
for role in ['owner', 'active', 'posting', 'memo']:
    pk = PasswordKey(account['name'], password, role=role, prefix=prefix)
    key_auths_public[role] = str(pk.get_public_key())
    key_auths_private[role] = str(pk.get_private_key())
    if role == "memo": 
        blk_auths_public[role] = str(account.json()["memo_key"])
    else:
        blk_auths_public[role] = str(account.json()[role]["key_auths"][0][0])

    if key_auths_public[role] != blk_auths_public[role]:
        sys.exit("Password provided is not correct. Public " + role + " key " + key_auths_public[role] + " doesn't match the one in the EFTG blockchain " + blk_auths_public[role])

data = {"name":account['name'],"wif":password,"owner":[{"type":"public","value":key_auths_public["owner"]},{"type":"private","value":key_auths_private["owner"]}],"active":[{"type":"public","value":key_auths_public["active"]},{"type":"private","value":key_auths_private["active"]}],"posting":[{"type":"public","value":key_auths_public["posting"]},{"type":"private","value":key_auths_private["posting"]}],"memo":[{"type":"public","value":key_auths_public["memo"]},{"type":"private","value":key_auths_private["memo"]}]}

print(json.dumps(data, indent=4))

# vim: set filetype=sh ts=4 sw=4 tw=0 wrap et:
