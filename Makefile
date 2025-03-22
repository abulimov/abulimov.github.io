BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/public
GITHUB_PAGES_BRANCH=master

help:
	@echo 'Makefile for a hugo Web site                                           '
	@echo '                                                                       '
	@echo 'Usage:                                                                 '
	@echo '   make clean                       remove the generated files         '
	@echo '   make publish                     generate site                      '
	@echo '   make github                      upload the web site via gh-pages   '
	@echo '   make redirect DEST=./some/path   update the redirects mirror        '
	@echo '                                                                       '
	@echo '                                                                       '

check:
	vale --minAlertLevel=error content/post
	@echo 'checking for bad links';\
	grep -P -R '^(?:(?!(\s*func|.*:=)).*)\[.+\]\((?:(?!http|\/)).+\)' content/post/;\
	EXIT_CODE=$$?;\
	if [ $$EXIT_CODE -eq 0 ]; \
	then \
		echo "found some bad links"; \
		exit 1; \
	else \
		echo "No bad links found"; \
	fi

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

publish: check
	hugo -b //bulimov.me/

github: publish
	ghp-import -m 'Updated blog' -b $(GITHUB_PAGES_BRANCH) $(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)

redirect: publish
ifndef DEST
	$(error DEST is undefined, usage: make redirect DEST=./path-to-dir)
endif
	./sync_links.py $(DEST)
