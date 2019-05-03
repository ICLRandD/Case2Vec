# Case2Vec

A simple web application for searching Word2Vec embeddings derived from approximately 2,000 law reports published by The Incorporated Council of Law Reporting for England & Wales (https://www.iclr.co.uk).

# Credit and acknowledgment

The Tornado web application included in this repository is heavily based on https://github.com/superkerokero/word2vec-search-app. Only minor modifications were made to the original codebase, including minor changes to `server.py`, `index.html` and `ajaxclient.js`. As such, we are very grateful to https://github.com/superkerokero for making the code available. 

# Usage
## Create a new virtual environment
1. Create a new virtual environment.
```python3 -m venv env```
2. Activate the virtual environemtn.
```source env/bin/activate```
## Install dependencies
```pip3 install -r requirements.txt```
## Decompress the vector file
Decompress ``common_sense_law_model_sm.txt.zip`
## Run `server.py`
In the terminal run `python server.py`
![screenshot1](img/screenshot1.png)
