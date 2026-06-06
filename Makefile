.PHONY: test audit smoke compile no-skip no-private-artifacts check

test:
	INTENTIA_ENV=test pytest -q

compile:
	python -m compileall -q src

no-skip:
	! grep -R "pytest.mark.skip\|pytest.mark.xfail\|@pytest.mark.skip\|@pytest.mark.xfail" tests

no-private-artifacts:
	! find . -path './.git' -prune -o -type f \( -name '*.py' -o -name '*.md' -o -name '*.json' -o -name '*.yml' -o -name '*.yaml'