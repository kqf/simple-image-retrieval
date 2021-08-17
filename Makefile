data/data.csv: data/output.txt data/*.py
	python data/fetch --targets $< --output $@

data/output.txt: data/*.py
	python data/explore.py --titles titles.txt --output $@

clean: 
	rm -rf output.txt

.PHONY: clean
