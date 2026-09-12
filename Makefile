PYTHON ?= python3
CXX ?= c++
SOURCE_DATE_EPOCH ?= 1789171200
TECTONIC ?= tectonic

PAPER_BUILD_DIR := .tmp-paper
PAPER_NAME := quaternary-covering-code-8-4-upper-bound-v0.1.0
PAPER_PDF := dist/paper/$(PAPER_NAME)-paper.pdf
PAPER_SOURCE := dist/paper/$(PAPER_NAME)-paper-source.tar.gz
RELEASE_DIR := dist/release

.NOTPARALLEL:

.PHONY: all test verify cpp evidence manifest paper-build paper-bundle \
	release-assets verify-release-assets check clean

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

paper-build:
	mkdir -p $(PAPER_BUILD_DIR)
	SOURCE_DATE_EPOCH="$(SOURCE_DATE_EPOCH)" FORCE_SOURCE_DATE=1 \
		XDG_CACHE_HOME="$$PWD/.tmp-tectonic-cache" \
		"$(TECTONIC)" -X compile paper/main.tex \
			--outdir $(PAPER_BUILD_DIR) --keep-logs
	test -s $(PAPER_BUILD_DIR)/main.pdf
	test "$$(head -c 5 $(PAPER_BUILD_DIR)/main.pdf)" = "%PDF-"
	! grep -E "Overfull|Underfull|LaTeX Warning|Undefined" \
		$(PAPER_BUILD_DIR)/main.log

paper-bundle:
	$(PYTHON) tools/build_paper_bundle.py

release-assets: check paper-build paper-bundle
	rm -rf $(RELEASE_DIR)
	mkdir -p $(RELEASE_DIR)
	cp $(PAPER_BUILD_DIR)/main.pdf $(PAPER_PDF)
	cp $(PAPER_PDF) $(PAPER_SOURCE) $(RELEASE_DIR)/
	cd $(RELEASE_DIR) && LC_ALL=C shasum -a 256 \
		$(notdir $(PAPER_PDF)) \
		$(notdir $(PAPER_SOURCE)) \
		> SHA256SUMS

verify-release-assets:
	$(PYTHON) tools/verify_release_assets.py

check: test verify cpp evidence
	$(PYTHON) verify_release_manifest.py \
		--manifest release-manifest.sha256 --require-git-completeness

clean:
	rm -rf .tmp-* dist __pycache__ tests/__pycache__ tools/__pycache__
