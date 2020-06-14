# Download atom from the website
$ sudo apt install ./Downloads/atom-amd64.deb

# Download Cloud SDK
# Add source
$ echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Get repo key
$ curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Install
$ sudo apt-get update && sudo apt-get install google-cloud-sdk

# Init profile
$ gcloud init

# Generate SSH key
$ ssh-keygen -t rsa -b 4096 -C "jmccall707@gmail.com"

# Add SSH key to github profile

# Install python3 venv
$ sudo apt install python3-venv

# Create venv
$ cd ~/Projects
$ python3 -m venv finny
$ cd ~/Projects/finny

# Clone repo
$ git clone git@github.com:jmccall/finny.git

# Activate venv
$ source ~Projects/finny/bin/activate

# Install deps
(vnenv)$ pip install -r requirements.txt

# Run app locally
(venv)$ python main.py
