# Simple image retreival [![tests](https://github.com/kqf/simple-image-retrieval/actions/workflows/ci.yml/badge.svg)](https://github.com/kqf/simple-image-retrieval/actions/workflows/ci.yml)

A boilerplate code to find similar images.


## Collect the data

See the scripts in the `data` folder, to start downloading do
```
make
```


## Tests
Start the tests on a toy example

```
pytest -s 
```

To check if the model overfits on the test data one can increase the number of epochs:

```bash
pytest -s tests/test_model.py --max-epochs 10

```
