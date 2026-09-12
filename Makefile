PYTHON ?= python3
CXX ?= c++

.NOTPARALLEL:

.PHONY: all test verify cpp evidence manifest check clean

all: check

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

verify:
	$(PYTHON) verify_code.py data/code-27.txt --expected-size 27
	$(PYTHON) independent_verify.py data/code-27.txt --expected-size 27
	$(PYTHON) analyze_near_cover.py data/near-cover-26-5-holes.txt
	$(PYTHON) independent_verify.py data/near-cover-26-5-holes.txt \
		--expected-size 26 --allow-invalid

cpp:
	mkdir -p .tmp-verifier
	$(CXX) -std=c++17 -O2 -Wall -Wextra -pedantic \
		verify_direct.cpp -o .tmp-verifier/verify_direct
	.tmp-verifier/verify_direct data/code-27.txt 27 4 0
	.tmp-verifier/verify_direct data/near-cover-26-5-holes.txt 26 5 5

evidence:
	$(PYTHON) audit_evidence.py

manifest:
	$(PYTHON) build_release_manifest.py

check: test verify cpp evidence
	$(PYTHON) verify_release_manifest.py \
		--manifest release-manifest.sha256 --require-git-completeness

clean:
	rm -rf .tmp-verifier __pycache__ tests/__pycache__
