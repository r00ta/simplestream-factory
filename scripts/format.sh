#!/bin/sh -e
set -x

uv run ruff format .
uv run ruff check --fix .
