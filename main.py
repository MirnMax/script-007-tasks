#!/usr/bin/env python3
import argparse
import os
import sys

import server.FileService as FileService


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
    params = parser.parse_args()

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
