import sys
from elcaminoreal.test import some_plugins

if __name__ != '__main__':
    raise ImportError("main module, not importable", __name__)

some_plugins.main(sys.argv)
