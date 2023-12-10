import os
import requests
from tqdm import tqdm
from urllib.parse import urlparse

def download_with_progress(url, file_name):
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024
    num_bars = int(file_size / chunk_size) if file_size > 0 else 1

    with open(file_name, 'wb') as file, tqdm(
        desc="Downloading",
        total=num_bars,
        unit="KB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=chunk_size):
            bar.update(len(data))
            file.write(data)

def get_game_path(game_name, download_option=True):
    game_name = game_name.replace(" ", "-").lower()
    url = f"https://www.coolmathgames.com/0-{game_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        lines = response.text.split("\n")
        found_game = False
        u = ''

        for line in lines[:500]:
            if '"game":{"u":"' in line or '"swf_1":{"width":"' in line:
                start_index = line.find('"u":"') + len('"u":"')
                end_index = line.find('"', start_index)
                u = line[start_index:end_index].replace("\\/", "/")
                found_game = True
                break

        if found_game:
            full_url = f"https://www.coolmathgames.com/{u}"
            print("Game Path URL:", full_url)

            if download_option:
                # Extract file name from URL
                file_name = os.path.basename(urlparse(full_url).path)

                print(f"Downloading {file_name}...")
                download_with_progress(full_url, file_name)
                return f"File downloaded: {file_name}"
            else:
                return "Download option disabled. Game path not downloaded."

        else:
            return "❗ Error: The game path could not be found in the response."

    except requests.exceptions.RequestException as e:
        return f"❗ Error: {e}"

if __name__ == "__main__":
    game_name_input = input("Enter the game name: ")
    
    # Ask the user if they want to download the file
    download_option = input("Do you want to download the file? (yes/no): ").lower() == "yes"
    
    result = get_game_path(game_name_input, download_option)
    print(result)
