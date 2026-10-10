TYPST ?= typst
SOURCE := docs/typst/main.typ
OUTPUT := docs/report/report.pdf

.PHONY: all pdf watch clean check-typst

all: pdf

check-typst:
	@command -v "$(TYPST)" >/dev/null 2>&1 || { \
		echo "Ошибка: Typst не найден. Установите Typst и повторите команду." >&2; \
		exit 1; \
	}

pdf: check-typst
	@mkdir -p docs/report
	$(TYPST) compile "$(SOURCE)" "$(OUTPUT)" --root .

watch: check-typst
	@mkdir -p docs/report
	$(TYPST) watch "$(SOURCE)" "$(OUTPUT)" --root .

clean:
	rm -f "$(OUTPUT)"
