# Financial_Dashboards_with_Streamlit

## For Portfolio to work:
I had to install gcc & XCode

## Youtube URL:
<https://www.youtube.com/watch?v=0ESc1bh3eIg&t=2627s>

## Documentation on streamlit
<https://docs.streamlit.io/en/stable/api.html>

## Documentation on stocktwit API
<https://api.stocktwits.com/developers/docs/api#streams-symbol-docs>

## Documentation for Tweepy API
<https://www.tweepy.org/>

## Documentation on reading from Reddit (wallstreetbets)
<https://www.reddit.com/dev/api/>

<https://praw.readthedocs.io/en/latest/getting_started/authentication.html>

#### Found code on implementing praw and scraping wallsterrt bets:
<https://medium.datadriveninvestor.com/scraping-wallstreetbets-for-stocks-signals-414e63ace210>

### To run dasboard via streamlit
`streamlit run <python_file_name.py>`

### How to deploy Streamlit App (to be verified)
<https://www.youtube.com/watch?v=jJTa625q85o>

## On Linux EC2:
Updaed VM: `sudo yum update`
Had to install Git: `sudo yum install git -y`
Had to install: `yum install gcc-c++`
Had to install Python 3.9:
```Linux
sudo yum install gcc openssl-devel bzip2-devel libffi-devel

sudo wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz

sudo tar xzf Python-3.9.0.tgz

cd Python-3.9.0

sudo ./configure --enable-optimizations 

sudo make altinstall

cd ..

sudo rm -f Python-3.9.0.tgz

python3.9 -V
```

But whenever you are going to close the SSH terminal window the process will stop and so will your app:
Here is the fix:
```
sudo yum install tmux

tmux new -s StreamSession

streamlit run dashboard.py
```

The next step is to detach our TMUX session so that it continues running in the background when you leave the SSH shell.
To do this just press Ctrl+B and then D (Don’t press Ctrl when pressing D)

To reattach session:
`tmux attach -t StreamSession`
