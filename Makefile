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
	@echo '                                                                       '
	@echo '                                                                       '

check:
	vale .
	@echo 'checking for bad links';\
	grep -P -R '\[.+\]\((?:(?!http|\/)).+\)' content/post/;\
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
	hugo -b //bulimov.ru/

github: publish
	ghp-import -m 'Updated blog' -b $(GITHUB_PAGES_BRANCH) $(OUTPUTDIR)
	git push origin $(GITHUB_PAGES_BRANCH)
