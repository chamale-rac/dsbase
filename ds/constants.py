BASES_PATH = 'bases/'
DATA_FILE_EXTENSION = '.json'
VERSION = 1
WHOAMI = 'admin'
SERVERS = ['Server1']

METADATA_TEMPLATE = {
    'version': VERSION,
    'tables': {},
    'whoami': WHOAMI,
    'status': {
        'servers': SERVERS,
        'servers_amount': len(SERVERS),
    }
}
METADATA_SAVE_NAME = 'metadata.json'

PRINT_DICTS_WITH = 'json'  # avaible 'json', 'yaml' or 'pprint'
