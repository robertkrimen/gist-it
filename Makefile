.PHONY: test t

test:
	unit2 discover -v test

t:
	cpanm --installdeps ./t
	prove t/
