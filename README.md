# UwU-downloader
dowenload mediacontent from gelbooru or e621 use simple terminal
## Instalation 
<details><summary>For windows</summary>

   1. Open powershell

   1. Download project
```
git clone https://github.com/Lorgar-Horusov/UwU-downloader
```

   3. Navigate to Directory: Change directories to the newly cloned repository:
```
cd \UwU-downloader
```

   4. Set Up Environment Variables: Create a file named .env (ensure the dot at the beginning) in the project directory using a text editor. Add the following lines, replacing the placeholders with your actual API keys and credentials (obtain these from the respective websites):
```
GELBOORU_API="Your API"
GELBOORU_USER_ID="Your User ID"
E621_API="Your API"
E621_LOGIN="Your Login"
```
   5. or use this commands
```
echo GELBOORU_API="Your API" >> .env
echo GELBOORU_USER_ID="Your User ID" >> .env
echo E621_API="Your API" >> .env
echo E621_LOGIN="Your Login" >> .env
```
   6. Create Virtual Environment: Create a virtual environment to isolate project dependencies:
```
python -m venv venv
```

   7. Activate Virtual Environment: Activate the virtual environment to use its packages:
```
venv\Scripts\activate
```

   8. Install Dependencies: Install the required Python libraries using pip:
```
pip install -r requirements.txt
```

   9. Run Downloader: Start the downloader script:
```
python main.py
```
</details>
