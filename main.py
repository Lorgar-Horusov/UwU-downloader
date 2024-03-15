import os
import json
import requests

from pathlib import Path
from alive_progress import alive_bar
from base64 import b64encode
from tabulate import tabulate
from colorama import Fore
from dotenv import load_dotenv
from art import tprint
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator, EmptyInputValidator


def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


clear()
tprint("UwU.py", font="Larry3d")
load_dotenv()

username = os.getenv('E621_LOGIN')
api_key = os.getenv('E621_API')
base_url_e621 = "https://e621.net/posts.json"
base_url_gelbooru = "https://gelbooru.com/index.php?page=dapi&s=post&q=index"

path_to_JSON = Path('response_JSON')
gelbooru_api = os.getenv("GELBOORU_API")
gelbooru_user_ID = os.getenv("GELBOORU_USER_ID")


def download_from_json(json_file, folder, total_files):
    with open(str(json_file), 'r') as file:
        data = json.load(file)

    with alive_bar(total_files, bar='circles', spinner='classic') as bar:
        for item in data['media']:
            url = item['url']
            name = f"{item['artist']}_{item['rating']}{Path(url).suffix}"
            file_path = Path(folder).joinpath(name)

            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                bar()
            else:
                print(f'Error downloading file {url}. Status code: {response.status_code}')


def request_to_gelbooru(tag: str, limit: int):
    """
        Sends a GET request to Gelbooru API to search for images with specified tags.
        Args:
            tag (str, definitely): search tags.
            limit (str, definitely): Number of results to retrieve.
        Returns:
            Json File
        Raises:
            requests.exceptions.RequestException: If there's an error with the request.
        """
    params = {
        "api_key": gelbooru_api,
        "user_id": gelbooru_user_ID,
        "tags": tag,
        "json": 1,
    }
    media_data = {'media': []}
    try:
        response = requests.get(f"{base_url_gelbooru}&limit={limit}", params=params)
        response.raise_for_status()
        data = response.json()
        table_data = []
        posts = data.get('post', [])
        for post in posts:
            tags = post.get('tags', {})
            artist = post.get('owner', {})
            rating = post.get('rating', {})
            file_url = post.get('file_url', {})
            rating_no_collar = ''

            if rating == 'sensitive':
                rating = f'{Fore.GREEN}safe{Fore.RESET}'
                rating_no_collar = 'safe'

            elif rating == 'questionable':
                rating = f'{Fore.YELLOW}questionable{Fore.RESET}'
                rating_no_collar = 'questionable'

            elif rating == 'explicit':
                rating = f'{Fore.RED}explicit{Fore.RESET}'
                rating_no_collar = 'explicit'

            elif rating == 'general':
                rating = f'{Fore.GREEN}general{Fore.RESET}'
                rating_no_collar = 'general'

            media_data['media'].append({'url': file_url, 'rating': rating_no_collar, 'artist': artist, 'tag': tags})

            with open(path_to_JSON, 'w') as json_file:
                json.dump(media_data, json_file, indent=2)

            tags_str = ''.join(tags)
            result = []

            for i in range(0, len(tags_str), 30):
                result.append(tags_str[i:i + 30])

            formatted_result = '\n'.join(result)
            table_data.append([file_url, formatted_result, ''.join(artist), rating])

            # Output tabular data
        headers = ["URL", "Tags", "Artist", "Rating"]
        print(tabulate(table_data, headers=headers, tablefmt="mixed_grid", stralign='center'))

    except requests.exceptions.RequestException as e:
        print(f"Error executing request: {e}")


def request_to_e621(tags: str, limit: int):
    """
        Sends a GET request to e621 API to search for images with specified tags.
        Args:
            tags (str, definitely): search tags..
            limit (str, definitely): Number of results to retrieve..
        Returns:
            Json File
        Raises:
            requests.exceptions.RequestException: If there's an error with the request.
        """

    media_data = {'media': []}
    # Form authorization header
    auth_header = f"{username}:{api_key}"
    encoded_auth_header = b64encode(auth_header.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_auth_header}",
        "User-Agent": "MyProject/1.0 (on behalf of user Lorgar Horusov)"
    }

    # Send GET request with parameters
    params = {
        'tags': tags,
        'limit': limit,
    }

    try:
        response = requests.get(base_url_e621, params=params, headers=headers)
        response.raise_for_status()  # Check for request errors
        data = response.json()

        posts = data.get('posts', [])

        # Prepare data for table output
        table_data = []
        rating_no_collar = ''

        for post in posts:
            file_info = post.get('file', {})
            file_url = file_info.get('url', '')
            tags = post.get('tags', {}).get('general', [])
            artist = post.get('tags', {}).get('artist', [])
            rating = post.get('rating', {})

            if rating == 'e':
                rating = f'{Fore.RED}explicit{Fore.RESET}'
                rating_no_collar = 'explicit'

            elif rating == 'q':
                rating = f'{Fore.YELLOW}questionable{Fore.RESET}'
                rating_no_collar = 'questionable'

            elif rating == 's':
                rating = f'{Fore.GREEN}safe{Fore.RESET}'
                rating_no_collar = 'safe'

            media_data['media'].append({'url': file_url, 'rating': rating_no_collar, 'artist': artist})

            with open(path_to_JSON, 'w') as json_file:
                json.dump(media_data, json_file, indent=2)

            # Format tag list
            tags_str = ', '.join(tags)
            result = []

            for i in range(0, len(tags_str), 30):
                result.append(tags_str[i:i + 30])

            formatted_result = '\n'.join(result)
            table_data.append([file_url, formatted_result, ', '.join(artist), rating])

        # Output tabular data
        headers = ["URL", "Tags", "Artist", "Rating"]
        print(tabulate(table_data, headers=headers, tablefmt="mixed_grid", stralign='center'))

    except requests.exceptions.RequestException as e:
        print(f"Error executing request: {e}")


def count_unique_urls(json_file):
    with open(str(json_file), 'r') as file:
        data = json.load(file)
        return sum(1 for item in data['media'] if 'url' in item)


def downloads():
    total_files = count_unique_urls(path_to_JSON)
    download = inquirer.confirm(message=f'Total files: {total_files}. Download?', default=False).execute()
    if download:
        home_path = Path(__file__).parent.joinpath('download folder')
        path = inquirer.filepath(message=f"Path to download folder'",
                                 default=str(home_path),
                                 validate=PathValidator(is_dir=True,
                                                        message="Input is not a directory")).execute()
        if path:
            download_from_json(path_to_JSON, path, total_files)


def main():
    try:
        menu = inquirer.select(
            message="Select site",
            choices=[
                "E621.net",
                "Gelbooru",
                Choice(value=None, name='Exit'),
            ],
            default=None
        ).execute()
        if menu == "E621.net":
            clear()
            tprint("e621 Downloader", font="Larry3d")
            tag = inquirer.text(message="Insert tags >>", default="").execute()
            count = inquirer.number(message="How much >>", min_allowed=1, max_allowed=500,
                                    validate=EmptyInputValidator(), default=None).execute()
            request_to_e621(tag, count)
            downloads()

        elif menu == "Gelbooru":
            clear()
            tprint("Gelbooru downloader", font="Larry3d")
            tag = inquirer.text(message="insert tags >>", default="").execute()
            count = inquirer.number(message="How much >>", min_allowed=1, max_allowed=500,
                                    validate=EmptyInputValidator(), default=None).execute()
            request_to_gelbooru(tag, count)

            downloads()

    except KeyboardInterrupt:
        clear()
        print("emergency program closing")


if __name__ == '__main__':
    main()
