#!/bin/sh
export BRIDG_ENV=testing
dropdb -h localhost -U postgres bridg-testing
createdb -h localhost -U postgres bridg-testing
python -m dev.migrate
python -m dev.seed
pytest -s ${@}
