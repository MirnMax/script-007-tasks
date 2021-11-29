import argparse
import logging
import logging.config
import os
import sys

import server.FileService as FileService


def setup_logger(level='NOTSET', filename=None):
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': level,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        config['root']['handlers'].append('file')
    logging.config.dictConfig(config)


def main():
    """Entry point of app.
    Get and parse command line parameters and configure web app.
    Command line options:
    -d --dir  - working directory (absolute or relative path, default: current_app_folder/data).
    -h --help - help.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='data', type=str,
                        help="working directory (default: 'data')")
    parser.add_argument('--log-level', default='warning', choices=['debug', 'info', 'warning', 'error'],
                        help='Log level to console (default is warning)')
    parser.add_argument('-l', '--log-file', type=str, help='Log file.')
    params = parser.parse_args()
    setup_logger(level=logging.getLevelName(params.log_level.upper()), filename=params.log_file)
    logging.debug('started')

    work_dir = params.dir if os.path.isabs(params.dir) else os.path.join(os.getcwd(), params.dir)
    FileService.change_dir(work_dir)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)