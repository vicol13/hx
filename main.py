

from search_engine.engine import  Engine
from json import dumps

def print_json(json):
    print(dumps(json,indent=4, sort_keys=True))

if __name__ == "__main__":
    e = Engine()
    print('----------------[brain]----------------')
    print_json(e.search('brain'))
    print('----------------[java]----------------')
    print_json(e.search('java'))
    print('----------------[bitcoin]----------------')
    print_json(e.search('bitcoin'))