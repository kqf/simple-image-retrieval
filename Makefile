message_limit = 100


all: data/positives/data.tsv data/anchors/data.tsv
	train --train_path data/positives/data.tsv --valid_path data/positives/data.tsv

data/positives/data.tsv: data/targets.txt data/positives.py
	python data/positives.py --target $< --output $@ --limit $(message_limit)

data/anchors/data.tsv: data/explored.tsv data/anchors.py
	python data/anchors.py --target $< --output $@ --limit $(message_limit)

data/explored.tsv: sources.csv data/explore.py
	python data/explore.py --source $< --output $@

clean: 
	rm -rf output.csv

clean-download:
	rm -rf data/photos

.PHONY: clean clean-download
