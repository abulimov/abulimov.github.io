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

check: publish
	vale --minAlertLevel=error content/post content/lists
	@echo
	@echo "Checking for bad links"
	./check_links.py content/post/* content/lists/*

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

publish:
	hugo --cleanDestinationDir -b //bulimov.me/

github: check publish
	ghp-import -m 'Updated blog' -b $(GITHUB_PAGES_BRANCH) $(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)

redirect: publish
ifndef DEST
	$(error DEST is undefined, usage: make redirect DEST=./path-to-dir)
endif
	./sync_links.py $(DEST)
