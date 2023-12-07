all: presentation.html

presentation.html: presentation.md style.css
	pandoc -t revealjs -so "$@" "$<"

clean:
	rm -rf *.html

.PHONY: clean
