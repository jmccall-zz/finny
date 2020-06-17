# Environment setup

**Download atom from the [website](https://atom.io)**

`$ sudo apt install ./Downloads/atom-amd64.deb`

**[Install Cloud SDK](https://cloud.google.com/sdk/docs/downloads-apt-get)**

**Init Cloud SDK profile**

`$ gcloud init`

**[Configure SSH for Github](https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)**

**Install python3 venv**

`$ sudo apt install python3-venv`

**Create python3 virtual env**
```
$ cd ~/Projects
$ python3 -m venv finny
$ cd ~/Projects/finny
```

**Clone app repository**

`$ git clone git@github.com:jmccall/finny.git`

**Activate venv**

`$ source ~Projects/finny/bin/activate`

**Install dependencies**

`(vnenv)$ pip install -r requirements.txt`

**Run app locally**

`(venv)$ python main.py`

# Documentation

[Quota API Google Doc](https://docs.google.com/document/d/1IlJgXWBHKrOYyDIayTwMn5FuKJ-GmBmTbT9VWNu2IS8/edit#heading=h.yoy3dee73fiw)

*   Contact `jmccall707@gmail.com` for access
