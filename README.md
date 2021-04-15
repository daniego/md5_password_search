# md5_password_search
Very first proof of concept to match a known md5'd "strings" against a lists of weak and hacked passwords.
First we generate an ElasticSearch index containing the plain text password and the md5'd one which later will be matched with your provided one.

### Requirements
```
pip install -r requirements.txt
```

### Load index
The `password_source` folder already contains a given source file with weak and leaked password.
You can add any text file that contains one password per line or just download some of many publicly available over the internet.
(danielmiessler/SecLists)[https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials] provides good examples.

By running
```
python generate_index.py -source=file
```
will scrape the mentioned folder

# Disclaimer
Any use of this POC is your responsibility!
