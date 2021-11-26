#!/usr/bin/env python3
import argparse
import os

import server.FileService as FileService


def main():
    """Entry point of app.
    Get and parse command line parameters and configure web app.
    Command line options:
    -d --dir  - working directory (absolute or relative path, default: current_app_folder/data).
    -h --help - help.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default=os.path.join(os.getcwd(), 'data'), type=str,
                        help="working directory (default: 'data')")

    params = parser.parse_args()
    FileService.change_dir(params.folder)


if __name__ == '__main__':
    main()
