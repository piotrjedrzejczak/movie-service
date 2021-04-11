# Movie Service

## Requirements

- Python 3.7.9+
- Registered API Key for IMDB Database  
    You can register for a key here: http://www.omdbapi.com/  
    Before using the application add your API key to  *config.py*

## Usage

```shell
-h,  --help             show this help message and exit
-t,  --titles           display the list of all movies
-tr, --top-rated        display the top rated movie/movies
-tb, --top-boxoffice    display the highest grossing movie
-a,  --avarage          display the avarage rating of all movies
-l   --list             list of movie titles to download
```

Download and store information of *The Matrix* and *Lord of the Rings*.

```shell
python ms.py --list "the matrix" "lord of the rings"
```

Now you can display the downloaded list of titles with:

```shell
python ms.py --titles
```

...and so on with the rest of the commands.