import os

import elcaminoreal

from elcaminoreal._args import argparser, argument

COMMANDS = elcaminoreal.Commands()

@COMMANDS.dependency()
def current_directory(_deps, _maybedeps):
    return '.'

@COMMANDS.dependency()
def environment(_deps, _maybedeps):
    return os.environ

@COMMANDS.dependency(dependencies=['environment', 'current_directory'])
def secret_filename(dependencies, _maybedeps):
    if 'VOYNICH_FILE' in dependencies['environment']:
        return dependencies['environment']['VOYNICH_FILE']
    return os.path.join(dependencies['current_directory'], 'voynich.json')

@COMMANDS.command(dependencies=['secret_filename'],
                  parser=argparser(
                      argument('--key-file', required=True),
                         ),
                 )
def create(args, dependencies):
    print("writing key to", args.key_file, "and public data to",
          dependencies['secret_filename'])

@COMMANDS.command(dependencies=['secret_filename'],
                  parser=argparser(
                      argument('--name', required=True),
                      argument('--value', required=True),
                         ),
                 )
def encrypt(args, dependencies):
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
    print("decrypting", dependencies['secret_filename'],
          "using", args.key_file,
          "into", args.directory)
