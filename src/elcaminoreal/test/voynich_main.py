if __name__ != '__main__':
    raise ImportError("Module should not be imported", __name__)

import sys

from elcaminoreal.test import voynich_skeleton

voynich_skeleton.COMMANDS.run(sys.argv[1:])
