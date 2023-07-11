.PHONY:extract
extract:
	pybabel extract --input-dirs=../../bot -o messages.pot --add-comments=NOTE --no-wrap

.PHONY:init
init:
	pybabel init -i messages.pot -d . -D messages -l en
	pybabel init -i messages.pot -d . -D messages -l ru
	pybabel init -i messages.pot -d . -D messages -l uk

.PHONY:update
update:
	pybabel update --no-wrap -d . -D messages -i messages.pot -N


.PHONY:extractnupdate
extractnupdate: extract update


.PHONY:compile
compile:
	pybabel compile -d . -D messages