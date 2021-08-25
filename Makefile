data/positives.csv: data/targets.txt data/positives.py
	python data/positives.py --target $< --output $@ --limit 100

data/data.csv: data/sources.txt data/*.py
	python data/anchors.py --target $< --output $@ --limit 10

data/sources.txt: titles.txt
	python data/explore.py --titles titles.txt --output $@

clean: 
	rm -rf output.txt

clean-download:
	rm -rf data/photos

.PHONY: clean clean-download
