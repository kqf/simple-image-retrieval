data/positives.tsv: data/targets.txt data/positives.py
	python data/positives.py --target $< --output $@ --limit 100

data/anchors.tsv: data/explored.tsv data/anchors.py
	python data/anchors.py --target $< --output $@ --limit 10

data/explored.tsv: sources.csv data/explore.py
	python data/explore.py --source $< --output $@

clean: 
	rm -rf output.csv

clean-download:
	rm -rf data/photos

.PHONY: clean clean-download
