# copy-folders-ssh
Simple script to copy folders via ssh with their paths given in a file.

# Usage
## Create a .env file inside the config folder with the following variables:

- `FILESNAMEPATH`: Path to a file to be read with your custom reader (more about this later) and which specifies which folders you want to copy
- `ROOTPATH`: Context path on server. Your file should give paths relative to this.
- `HOST`: Host on which the desired folders are
- `USR`: User to ssh to host
- `PASSWD`: SSH password

## Running
Call python (or python3) with the following flags:

- `--mode`: specifies to which machine you want to copy files to. 'local' to local machine and 'remote' to host machine.
- `--path`: path where to put copied folders

## Readers
For the script to work, you need to give a Reader that inherite from `BaseReader` and implement a `readline` method. Each return of `readline()` should give the relative (to the `ROOTPATH` var) path of the desired folder. The folder and it's contents will be copied to the path provided with the --path flag, as well as it's parent directories up to the `ROOTPATH`.

# TODO
- [ ] Allow paths with blank spaces
- [ ] Validate given paths to not allow improper path representation
- [ ] Allow passless ssh
- [ ] Implement option to search for a given directory without knowing the path from `ROOTPATH` to it
- [ ] Modularize and upload to PyPi