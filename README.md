# Environment setup

**Download atom from the [website](https://atom.io)**

`$ sudo apt install ./Downloads/atom-amd64.deb`

**[Install Cloud SDK](https://cloud.google.com/sdk/docs/downloads-apt-get)**

**Init Cloud SDK profile**

`$ gcloud init`

**[Configure SSH for Github](https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)**

**Install python3 venv**

`$ sudo apt install python3-venv`

**Clone app [repository](https://github.com/jmccall/finny)**
```
cd $PROJECT_DIR
$ git clone git@github.com:jmccall/finny.git
```

**Create python3 virtual env**
```
$ cd $PROJECT_DIR/finny
$ python3 -m venv venv
```

**Activate venv**

`$ source venv/bin/activate`

**Install dependencies**

`(vnenv)$ pip install -r requirements.txt`

**Run app locally**

`(venv)$ python main.py`

# Documentation

[Quota API Google Doc](https://docs.google.com/document/d/1IlJgXWBHKrOYyDIayTwMn5FuKJ-GmBmTbT9VWNu2IS8/edit#heading=h.yoy3dee73fiw)

*   Contact `jmccall707@gmail.com` for access

[IEX Proxy Logic (Lucid charts)](https://app.lucidchart.com/documents/view/b999b045-3b5b-4d9d-9e16-2d1524a5bbdb/0_0)
