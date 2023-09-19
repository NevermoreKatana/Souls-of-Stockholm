#!/bin/bash

# Установить Poetry Preview с помощью curl
curl -sSL https://install.python-poetry.org | POETRY_PREVIEW=1 python3 - && make install
