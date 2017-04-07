# Pylasic
#### Prerequsitc
1. Python > 2.7
2. Flask
    ```
    pip install flask
    ```
3. Elastic Runtime
```
Download: https://www.elastic.co/downloads/elasticsearch
Document: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
```

#### Setup server
Default port 5000
```
cd pylastic/flask
./start_debug.sh
```
This script will bring up a server.
Now in broswer: http://127.0.0.1:5000/

### Example
Try type anythins in search box and press Enter.
```
dataset1 = {
    'title': '1st dataset',
    'text': "I'm the first data set"
}

dataset2 = {
    'title': '2nd dataset',
    'text': "I'm the second data set"
}

dataset3 = {
    'title': '3rd dataset',
    'text': "I'm the third data set"
}
```
==================================================================================

conda install -c conda-forge elasticsearch=5.3.0
or 
pip install elasticsearch
