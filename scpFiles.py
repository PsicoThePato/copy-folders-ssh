import subprocess
import argparse

from fabric import Connection

from config import CONNECTION_PARAMS, FILENAMESPATH, ROOTPATH
from custom_readers import date_hierarchy_reader
import base_reader


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
                target_folder = target_root_directory + subdirectory
                if " " in target_folder:
                    raise ValueError(
                        "Blank spaces are not permitted on target_folder"
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
                            f"{CONNECTION_PARAMS.usr}@{CONNECTION_PARAMS.host}:{ROOTPATH}/{subdirectory}/*",
                            target_folder,
                        ],
                        check=True,
                    )


if __name__ == "__main__":
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
        dest="target_root_path",
        required=True,
        help="Root folder to copy files/folders",
    )
    args = parser.parse_args()
    print(args.mode, args.target_root_path)

    reader = date_hierarchy_reader.DateHierarchyReader(FILENAMESPATH)
    copy_from_csv(args.mode, args.target_root_path, reader)
