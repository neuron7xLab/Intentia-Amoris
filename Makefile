.PHONY: test audit smoke compile

test:
	INTENTIA_ENV=test pytest -q

compile:
	python -m compileall -q src

audit:
	intentia-product-audit
	intentia-security-audit

smoke:
	intentia-value

all: compile test audit smoke
