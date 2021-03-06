import sys
import json
import codecs
from re import sub
from argparse import ArgumentParser, Namespace
from typing import Optional
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import URLError
from sqlite3 import (
    IntegrityError,
    Connection,
    Cursor,
    connect
)
from config import (
    API_KEY,
    INSERT_INTO_MOVIES_TABLE,
    REQUIRED_FIELDS,
    CHECK_IF_MOVIES_TABLE_EXIST,
    CREATE_MOVIES_TABLE,
    SELECT_ALL_TITLES,
    SELECT_AVARAGE_RATING,
    SELECT_HIGHEST_BOXOFFICE,
    SELECT_HIGHEST_RATED_MOVIE,
    UPDATE_MAIN_TABLE_RECORD,
)


def search_movies(list_of_movies: list, db_uri: str) -> None:
    connection = connect(db_uri)
    with connection:
        for title in list_of_movies:
            try:
                raw_results = get_movie_details_by_title(title, REQUIRED_FIELDS, API_KEY)
                reformatted = format_movie_data(raw_results, REQUIRED_FIELDS)
                db_operation(connection, INSERT_INTO_MOVIES_TABLE, movie=reformatted)
                print(f"Found {title}, saving to database...")
            except ConnectionRefusedError as e:
                print(e)
            except LookupError:
                print(f"Sorry, {title} not found")
            except IntegrityError as error:
                if "UNIQUE" in str(error.args):
                    print(f"You already have {title} in your database, updating details...")
                    reformatted.append(reformatted.pop(0))
                    db_operation(connection, UPDATE_MAIN_TABLE_RECORD, movie=reformatted)
    connection.close()


def display_movies(db_uri: str, sql: str) -> None:
    connection = connect(db_uri)
    with connection:
        cursor = db_operation(connection, sql)
        for record in cursor.fetchall():
            print(' '.join([str(field) for field in record]))
    connection.close()


def get_movie_details_by_title(title: str, required_fields: list, apikey: str) -> dict:
    title = quote(title)
    uri = f"http://www.omdbapi.com/?t={title}&apikey={apikey}"
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
            return {key: data.get(key) for key in required_fields}
    except URLError as e:
        if hasattr(e, "reason"):
            raise ConnectionError(f"Failed to reach a server. Reason: {e.reason}")
        elif hasattr(e, "code"):
            raise ConnectionError(f"Server could not fulfill the request. Error code: {e.code}")


def format_movie_data(data: dict, required_fields: list) -> list:
    for key, value in data.items():
        if value == "N/A":
            data[key] = None
            continue
        if key == "imdbRating":
            data[key] = float(value)
        if key == "BoxOffice":
            data[key] = int(sub(r"[^\d]", "", value))
    return [data.get(key) for key in required_fields]


def db_operation(connection: Connection, sql: str, movie: Optional[list] = None) -> Cursor:
    cursor = connection.cursor()
    if movie:
        cursor.execute(sql, movie)
    else:
        cursor.execute(sql)
    return cursor


def parse_args(args: list) -> Namespace:
    parser = ArgumentParser(prog="movie-service")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-t",
        "--titles",
        action="store_true",
        help="display the list of all movies"
    )
    group.add_argument(
        "-tr",
        "--top-rated",
        action="store_true",
        help="display the top rated movie/movies"
    )
    group.add_argument(
        "-tb",
        "--top-boxoffice",
        action="store_true",
        help="display the highest grossing movie"
    )
    group.add_argument(
        "-a",
        "--avarage",
        action="store_true",
        help="display the avarage rating of all movies"
    )
    group.add_argument(
        "-l",
        "--list",
        nargs="+",
        help="list of movie titles to download"
    )
    return parser.parse_args(args)


def main(args: list, db_uri: str = None):
    if not db_uri:
        from config import DATABASE_URI
        db_uri = DATABASE_URI
    connection = connect(db_uri)
    cursor = db_operation(connection, CHECK_IF_MOVIES_TABLE_EXIST)
    if not cursor.fetchall():
        db_operation(connection, CREATE_MOVIES_TABLE)
    connection.close()

    parser = parse_args(args)
    if parser.list:
        search_movies(parser.list, db_uri)
    elif parser.titles:
        display_movies(db_uri, SELECT_ALL_TITLES)
    elif parser.top_rated:
        display_movies(db_uri, SELECT_HIGHEST_RATED_MOVIE)
    elif parser.top_boxoffice:
        display_movies(db_uri, SELECT_HIGHEST_BOXOFFICE)
    elif parser.avarage:
        display_movies(db_uri, SELECT_AVARAGE_RATING)


if __name__ == "__main__":
    main(sys.argv[1:])
