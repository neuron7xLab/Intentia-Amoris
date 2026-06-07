.RECIPEPREFIX := >
.PHONY: compile test verify check all

compile:
>python -m compileall -q src

test:
>pytest -q

verify:
>bash scripts/verify_all.sh

check: verify

all: check
