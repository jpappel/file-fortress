all: presentation.html

presentation.html: presentation.md style.css
	pandoc -t revealjs --slide-level=2 -so "$@" "$<"

clean:
	rm -rf *.html

.PHONY: clean
