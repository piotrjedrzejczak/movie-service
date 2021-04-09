import argparse
import sys
from config import *


def parse_args(args):
    parser = argparse.ArgumentParser(prog="movie-service")
    parser.add_argument("list", nargs="+", help="list of movie titles to download")
    return parser.parse_args(args)


if __name__ == "__main__":
    parse_args(sys.argv[1:])
