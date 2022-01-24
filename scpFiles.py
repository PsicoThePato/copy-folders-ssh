import subprocess
import argparse
import re

from fabric import Connection

from config import CONNECTION_PARAMS, FILENAMESPATH, ROOTPATH
from custom_readers import date_hierarchy_reader
import base_reader


def get_treated_path(path: str, validate: bool=True):
    valid_path_re_str = r'^(\/+|[\.\w]+)+$'
    valid_path = re.compile(valid_path_re_str)
    if validate:
        if not valid_path.match(path):
            raise ValueError(
                fr"""
                {path} is an invalid path
                Use full or relative paths with slashs ('/') as
                the directory delimiter and without any blank space.
                The validating regex used is as follows:
                {valid_path_re_str}
                If you believe this validation to not be necessary, run with the --force flag.
                """
                )
        if path == '/':
            raise ValueError(
                """
                Trying to copy the ENTIRE server.
                If you really want to do this, use the --force flag.
                """
            )
    if path[-1] != '/':
        path = path + '/'
    return path


def copy_from_csv(mode: str, target_root_directory: str, reader: base_reader.BaseReader):
    with open(FILENAMESPATH, "r") as f:
        _ = f.readline()
        with Connection(
            host=CONNECTION_PARAMS.host,
            user=CONNECTION_PARAMS.usr,
            connect_kwargs={
                "password": CONNECTION_PARAMS.passwd,
                "key_filename": None,
            },
        ) as connection:
            while subdirectory := reader.readline():
                # adding backslash in case user forgot
                if subdirectory[-1] != '/':
                    subdirectory = subdirectory + '/'
                target_folder = target_root_directory + subdirectory
                if " " in target_folder:
                    raise ValueError(
                        "Blank spaces are not permitted on paths"
                    )

                mkdir_command = f"mkdir -p {target_folder}"
                if mode == "remote":
                    connection.run(mkdir_command)
                    connection.run(
                        f"cp {ROOTPATH}/{subdirectory}* '{target_folder}'"
                    )
                elif mode == "local":
                    subprocess.run(str.split(mkdir_command, " "), check=True)
                    subprocess.run(
                        [
                            "sshpass",
                            "-p",
                            CONNECTION_PARAMS.passwd,
                            "scp",
                            f"{CONNECTION_PARAMS.usr}@{CONNECTION_PARAMS.host}:{ROOTPATH}/{subdirectory}*",
                            target_folder,
                        ],
                        check=True,
                    )


def dry_run(mode:str, target_root_directory: str, reader: base_reader.BaseReader):
    pass


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        action="store",
        dest="mode",
        required=True,
        help="local to copy to local machine; remote to copy to remote machine",
    )
    parser.add_argument(
        "--path",
        action="store",
        dest="target_root_directory",
        required=True,
        help="Root folder to copy files/folders",
    )
    parser.add_argument('--force', dest='validate', action='store_false')
    parser.add_argument('--dry-run', dest='run', action='store_false')

    parser.set_defaults(validate=True, run=True)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    reader = date_hierarchy_reader.DateHierarchyReader(FILENAMESPATH)
    treated_path = get_treated_path(args.target_root_directory, args.validate)
    copy_from_csv(args.mode, treated_path, reader)
