import os
import json
import requests
import keyboard

from pathlib import Path
from alive_progress import alive_bar
from base64 import b64encode
from tabulate import tabulate
from colorama import Fore
from dotenv import load_dotenv
from art import tprint


def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


clear()
tprint("e621 Downloader", font="Larry3d")
load_dotenv()

username = os.getenv('E621_LOGIN')
api_key = os.getenv('E621_API_KEY')
base_url = "https://e621.net/posts.json"
path_to_JSON = Path('response_JSON')


def download_urls(url, folder, name):
    response = requests.get(url)
    if response.status_code == 200:
        # Extract filename from URL
        file_path = folder / Path(name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f'Error downloading file {url}. Status code: {response.status_code}')


def download_from_json(json_file, folder, total_files):
    with open(str(json_file), 'r') as file:
        data = json.load(file)
        with alive_bar(total_files, bar='circles', spinner='classic') as bar:
            for item in data['media']:
                name = f"{item['artist']}_{item['rating']}{Path(item['url']).suffix}"
                download_urls(item['url'], folder, name=name)
                bar()


def request_to_e621(tags='', limit='1'):
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
        response = requests.get(base_url, params=params, headers=headers)
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


def main():
    tag = input('Insert tags: [>>] ')
    limits = input('How much: [>>] ')
    request_to_e621(tag, limits)
    total_files = count_unique_urls(path_to_JSON)
    print(f'Total files: {total_files}.\nDownload yes/no?')

    while True:
        user_input = keyboard.read_event(suppress=True).name.lower()

        if user_input == 'y':
            download_folder = Path('C:/Users/user/PycharmProjects/e621_send/download folder')
            download_from_json(path_to_JSON, download_folder, total_files=total_files)
            print('Download completed')
            break

        elif user_input == 'n':
            print('Download cancelled')
            break

        else:
            print('Invalid input.')


if __name__ == '__main__':
    main()
