prod: convert_readme test
	python setup.py sdist upload -r pypi

test: convert_readme
	python setup.py sdist upload -r pypitest

convert_readme: 
	pandoc --from=markdown --to=rst --output=README.rst README.md
