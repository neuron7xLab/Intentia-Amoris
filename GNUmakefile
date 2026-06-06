.RECIPEPREFIX := >
.PHONY: compile test check all

compile:
>python -m compileall -q src

test:
>pytest -q

check: compile test

all: check
