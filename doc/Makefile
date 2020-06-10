all: doc

doc:
	# prerequisites for building docs:
	#  pacman -S asciidoctor (or your OS's equivalent)
	#  gem install pygments.rb
	mkdir -p dist/latest/
	asciidoctor -a docinfo -a stylesheet! -o dist/latest/index.html content.adoc
	cp -r assets dist/latest/

github: doc
	# prerequisites for pushing docs:
	#  pip install ghp-import
	ghp-import -m "Generate documentation" -b gh-pages dist/
	git push origin gh-pages
