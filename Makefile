output.txt: data/*.py
	python data/explore.py --titles titles.txt --output $@

clean: 
	rm -rf output.txt

.PHONY: clean
