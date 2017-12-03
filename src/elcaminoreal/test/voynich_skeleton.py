"""
Skeleton for Voynich

Voynich is a system for encrypting secrets.
This is a rough skeleton, to show-case how elcaminoreal
would work for a real command.
"""
import os

import elcaminoreal

from elcaminoreal._args import argparser, argument

COMMANDS = elcaminoreal.Commands()

@COMMANDS.dependency()
def current_directory(_deps, _maybedeps):
    """
    Current working directory
    """
    return '.'

@COMMANDS.dependency()
def environment(_deps, _maybedeps):
    """
    Environment dictionary
    """
    return os.environ

@COMMANDS.dependency(dependencies=['environment', 'current_directory'])
def secret_filename(dependencies, _maybedeps):
    """
    The filename to put the encrypted secrets in.
    """
    if 'VOYNICH_FILE' in dependencies['environment']:
        return dependencies['environment']['VOYNICH_FILE']
    return os.path.join(dependencies['current_directory'], 'voynich.json')

@COMMANDS.command(dependencies=['secret_filename'],
                  parser=argparser(
                      argument('--key-file', required=True),
                  ),
                 )
def create(args, dependencies):
    """
    Create a new secrets file (and save the private key).
    """
    print("writing key to", args.key_file, "and public data to",
          dependencies['secret_filename'])

@COMMANDS.command(dependencies=['secret_filename'],
                  parser=argparser(
                      argument('--name', required=True),
                      argument('--value', required=True),
                  ),
                 )
def encrypt(args, dependencies):
    """
    Add a new encrypted secret to the dependencies.
    """
    print("adding to", dependencies['secret_filename'],
          "name", args.name,
          "value", args.value)

@COMMANDS.command(dependencies=['secret_filename'],
                  parser=argparser(
                      argument('--key-file', required=True),
                      argument('--directory', required=True),
                  ),
                 )
def decrypt(args, dependencies):
    """
    Decrypt the secrets from a file into a directory
    """
    print("decrypting", dependencies['secret_filename'],
          "using", args.key_file,
          "into", args.directory)
