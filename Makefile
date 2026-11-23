# Unbreaking Software site
include mccole/mccole.mk

DATABASES := sql/lab.db sql/penguins.db sql/survey.db

## db: rebuild databases
db: ${DATABASES}

sql/lab.db: bin/create_sql_lab.sql
	@rm -f $@
	sqlite3 $@ < $<

sql/penguins.db: bin/create_sql_penguins.py data/penguins.csv data/geography.csv
	@rm -f $@
	python $< $@ data/penguins.csv data/geography.csv

sql/survey.db: bin/create_sql_survey.py
	@rm -f $@
	python $< $@ 192837
