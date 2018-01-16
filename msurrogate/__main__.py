"""
"""
from __future__ import division, print_function, unicode_literals
import argparse
import Pyro4
import json

from .pyro4_superproxy import SuperProxy

if __name__ == '__main__':
    Pyro4.config.SERIALIZERS_ACCEPTED = ['json', 'marshal', 'serpent', 'pickle', 'dill']
    #Pyro4.config.REQUIRE_EXPOSE = False
    daemon   = Pyro4.Daemon()

    print("server object uri:", factory.uri)

    json_conn_conf = dict(
        v1 = str(factory.uri),
    )

    with open('iirrational_pyro_con.json', 'w') as F:
        json.dump(
            json_conn_conf, F,
            indent = 4,
            sort_keys = True,
        )

    daemon.requestLoop()
