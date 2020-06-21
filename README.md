# Infra set up

## GCP App Engine

This service runs as a Python3 [Flask](https://flask.palletsprojects.com/en/1.1.x/)
app on [GCP App Engine](https://cloud.google.com/appengine/docs/standard/python3).

## [Firestore](https://cloud.google.com/appengine/docs/standard/python3/using-cloud-datastore)

Firestore DB runs in the same GCP project and is used to store fin info. The
IEX views are configured with "freshness" configs so instead of hitting the
IEX Cloud endpoint every time and blowing through usage quota, we just go to
Firestore.


# Environment setup

## Setup atom ([website for download](https://atom.io))

`$ sudo apt install ./Downloads/atom-amd64.deb`

## [Install Cloud SDK](https://cloud.google.com/sdk/docs/downloads-apt-get)

```
# Init gcloud
$ gcloud init

# Install datastore emulator
$ sudo apt install google-cloud-sdk-datastore-emulator
```

## [Configure SSH for Github](https://help.github.com/en/enterprise/2.17/user/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## Dev env setup

1.  `$ sudo apt install python3-venv`

2.  **Clone app [repository](https://github.com/jmccall/finny)**
    ```
    cd $PROJECT_DIR
    $ git clone git@github.com:jmccall/finny.git
    ```

3.  Create python3 virtual env**
    ```
    $ cd $PROJECT_DIR/finny
    $ python3 -m venv venv
    ```

4.  Activate venv**
    `$ source venv/bin/activate`

5.  Install dependencies**
    `$(vnenv) pip install -r requirements.txt`

6.  Run app locally**
    `$(venv)$ python main.py`

# Documentation

[Quota API Google Doc](https://docs.google.com/document/d/1IlJgXWBHKrOYyDIayTwMn5FuKJ-GmBmTbT9VWNu2IS8/edit#heading=h.yoy3dee73fiw)

*   Contact `jmccall707@gmail.com` for access

[IEX Proxy Logic (Lucid charts)](https://app.lucidchart.com/documents/view/b999b045-3b5b-4d9d-9e16-2d1524a5bbdb/0_0)

## Services

### IEX

Forward proxy to [IEX Cloud API](https://iexcloud.io/docs/api/).

Usage: https://finyee.wl.r.appspot.com/iex/stable/stock/{symbol}/latestPrice

## Test locally
```
# Set app default creds so you can connect to firestore
$ export GOOGLE_APPLICATION_CREDENTIALS=<service account key path>

# Run it
$(venv) python main.py
```
