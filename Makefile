message_limit = 100

data/positives.tsv: data/targets.txt data/positives.py
	python data/positives.py --target $< --output $@ --limit $(message_limit)

data/anchors.tsv: data/explored.tsv data/anchors.py
	python data/anchors.py --target $< --output $@ --limit $(message_limit)

data/explored.tsv: sources.csv data/explore.py
	python data/explore.py --source $< --output $@

clean: 
	rm -rf output.csv

clean-download:
	rm -rf data/photos

.PHONY: clean clean-download
