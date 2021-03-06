all: init docs test

init:
	python setup.py develop
	pip install tox coverage Sphinx

test:
	coverage erase
	tox
	coverage html

docs: documentation

documentation:
	python setup.py build_sphinx

messages:
	python translations.py make

compilemessages:
	python translations.py compile

upload:
	python setup.py sdist --formats=gztar register upload
