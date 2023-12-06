from functools import reduce
from os.path import dirname

root_directory = reduce(lambda x, _: dirname(x), range(3), __file__)