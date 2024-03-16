# UwU-downloader
dowenload mediacontent from gelbooru or e621 use simple terminal
## Instalation 

###for windows

Open powershell

Download project
```
git clone https://github.com/Lorgar-Horusov/UwU-downloader
```

Navigate to Directory: Change directories to the newly cloned repository:
```
cd \UwU-downloader
```

Set Up Environment Variables: Create a file named .env (ensure the dot at the beginning) in the project directory using a text editor. Add the following lines, replacing the placeholders with your actual API keys and credentials (obtain these from the respective websites):
```
GELBOORU_API="Your API"
GELBOORU_USER_ID="Your User ID"
E621_API="Your API"
E621_LOGIN="Your Login"
```
or use this commands
```
echo GELBOORU_API="Your API" >> .env
echo GELBOORU_USER_ID="Your User ID" >> .env
echo E621_API="Your API" >> .env
echo E621_LOGIN="Your Login" >> .env
```
Create Virtual Environment: Create a virtual environment to isolate project dependencies:
```
python -m venv venv
```

Activate Virtual Environment: Activate the virtual environment to use its packages:
```
venv\Scripts\activate
```

Install Dependencies: Install the required Python libraries using pip:
```
pip install -r requirements.txt
```

Run Downloader: Start the downloader script:
```
python main.py
```

