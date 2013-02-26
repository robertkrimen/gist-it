.PHONY: test t crunch

test:
	unit2 discover -v test
	@echo
	@echo "For remote testing with perl, run the following:"
	@echo "   dev_appserver.py ."
	@echo "   $(MAKE) t"

t:
	mkdir -p t/p5
	perl t/cpanm -l t/p5 --installdeps ./t
	prove t/
