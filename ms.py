import sys
import json
import codecs
from argparse import ArgumentParser, Namespace
from sqlite3 import connect, Connection, IntegrityError
from typing import Optional
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import URLError
from config import (
    API_KEY,
    INSERT_INTO_MOVIES_TABLE,
    REQUIRED_FIELDS,
    CHECK_IF_MOVIES_TABLE_EXIST,
    CREATE_MOVIES_TABLE,
    UPDATE_MAIN_TABLE_RECORD,
)


def get_movie_details_by_title(title: str, required_fields: list) -> dict:
    title = quote(title)
    uri = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    req = Request(uri)
    try:
        with urlopen(req) as response:
            charset = response.headers.get_param("charset")
            try:
                reader = codecs.getreader(charset)
            except LookupError:
                reader = codecs.getreader("utf-8")
            data = json.load(reader(response))
            if data.get("Error"):
                raise LookupError("Movie Not Found!")
            return [data.get(key) for key in required_fields]
    except URLError as e:
        if hasattr(e, "reason"):
            print(f"Failed to reach a server. Reason: {e.reason}")
        elif hasattr(e, "code"):
            print(f"Server could not fulfill the request. Error code: {e.code}")


def search_movies(list_of_movies: list, db_uri: str) -> None:
    connection = connect(db_uri)
    with connection:
        cursor = db_operation(connection, CHECK_IF_MOVIES_TABLE_EXIST)
        if not cursor.fetchall():
            db_operation(connection, CREATE_MOVIES_TABLE)
        for title in list_of_movies:
            try:
                result = get_movie_details_by_title(title, REQUIRED_FIELDS)
            except LookupError:
                print(f"{title} not found.")
            try:
                db_operation(connection, INSERT_INTO_MOVIES_TABLE, movie=result)
            except IntegrityError as error:
                if "UNIQUE" in str(error.args):
                    result.append(result.pop(0))
                    db_operation(connection, UPDATE_MAIN_TABLE_RECORD, movie=result)
    connection.close()


def db_operation(connection: Connection, sql: str, movie: Optional[list] = None):
    cursor = connection.cursor()
    if movie:
        cursor.execute(sql, movie)
    else:
        cursor.execute(sql)
    return cursor


def parse_args(args: list) -> Namespace:
    parser = ArgumentParser(prog="movie-service")
    parser.add_argument("list", nargs="+", help="list of movie titles to download")
    return parser.parse_args(args)


def main(args: list, db_uri: str = None):
    parser = parse_args(args)
    if not db_uri:
        from config import DATABASE_URI
        db_uri = DATABASE_URI
    if parser.list:
        search_movies(parser.list, db_uri)


if __name__ == "__main__":
    main(sys.argv[1:])
