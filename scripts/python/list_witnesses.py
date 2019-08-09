#!/usr/bin/env python3
from beem.witness import ListWitnesses
from beem.instance import set_shared_steem_instance

from beem import Steem
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

print(ListWitnesses())
