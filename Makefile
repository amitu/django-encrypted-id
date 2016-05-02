.PHONY: tests tests0

tests0:
	tox -e py27-django15

tests:
	tox

release:
	python setup.py bdist_wheel sdist --formats=bztar,zip upload

clean:
	rm -rf .tox
