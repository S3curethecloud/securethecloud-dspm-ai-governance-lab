PYTHON ?= python
PORT ?= 8015

.PHONY: install test validate evidence run all

install:
	$(PYTHON) -m pip install -r backend/requirements.txt

test:
	pytest backend/tests -q

validate:
	$(PYTHON) scripts/validate_repo.py

evidence:
	$(PYTHON) scripts/generate_evidence.py

run:
	uvicorn backend.app.main:app --reload --port $(PORT)

all: validate test evidence
