# The Imdb API

## Prerequisites
1. `docker` environment
2. `docker-compose`
3. Python 3.9 for development


## Development

### 1. Create and update local .env

``` Bash
cp .env.example .env
```

### 2. Setup virtual env and install dependencies
``` Bash
> python -m venv venv
> source ./venv/bin/activate
> pip install pip-tools
> make dependencies
```

### 3. Run dev version, please refer to the Makefile for other options and operations.
``` Bash
> make devlocal 
```

Then open `http://localhost:<port_defined_in_env>/api/docs`

### 4. Setup Development Environment for IDEs
After running #2
``` Bash
> pip-sync requirements-dev.txt
> code .
```

### 5. query LIMIT for wikidata moview in directory "app.apis.wikidata" was reduced to 3 for test purposes only, and can be increased to 10000 for normal operation 