import argparse
import sys
import json
import codecs
from urllib import parse, request
from config import API_KEY


def parse_args(args: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="movie-service")
    parser.add_argument(
        "list",
        nargs="+",
        help="list of movie titles to download"
    )
    return parser.parse_args(args)


def get_movie_details(title: str, required_fields: list):
    title = parse.quote(title)
    uri = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    req = request.Request(uri)
    with request.urlopen(req) as response:
        if response.code == 200:
            charset = response.headers.get_param('charset')
            try:
                reader = codecs.getreader(charset)
            except LookupError:
                reader = codecs.getreader("utf-8")
            data = json.load(reader(response))
            return {key: data.get(key) for key in required_fields}


if __name__ == "__main__":
    parse_args(sys.argv[1:])
