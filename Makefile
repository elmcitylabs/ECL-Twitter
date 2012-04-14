all: pyc version push

init:
	virtualenv .
	. bin/activate && python setup.py develop

pyc:
	find . -name "*.pyc" -exec rm '{}' ';'

version: pyc
	echo "Packaging version ${MAJ}.${MIN}"
	sed -i '' 's/\(__version__ = \).*/\1"${MAJ}.${MIN}"/g' ecl_twitter/metadata.py
	sed -i '' 's/\(version = \).*/\1"${MAJ}"/g' docs/conf.py
	sed -i '' 's/\(release = \).*/\1"${MAJ}.${MIN}"/g' docs/conf.py
	git add ecl_twitter/metadata.py
	git add docs/conf.py
	git commit -m "bump version to ${MAJ}.${MIN}"
	python setup.py sdist upload --sign
	s3cmd put dist/ecl_twitter-${MAJ}.${MIN}.tar.gz s3://packages.elmcitylabs.com/ -P

documentation:
	cd docs && make html && cd _build/html && git add . && git commit -m "doc update" && git push
	python setup.py upload_docs

push:
	git push github master
	git push origin master

