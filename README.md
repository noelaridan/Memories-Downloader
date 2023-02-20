# Memories Downloader
Python script allows you to automatically download all the memories from your Snapchat account using the JSON file of your exported data.

The metadata for each photo or video is also set based on the date and location specified in the JSON file.

## Prerequisites
- Python 3.x
- [Exiftool](https://exiftool.org/install.html)

## Installation
1. Download the file `memories_downloader.py` in the directory of your choice.
2. Install Exiftool by following the instructions available on [this page](https://exiftool.org/install.html).
3. Install the Python dependencies by running the following command:
```bash
pip install requests
```

## Usage
1. Export your Snapchat data by following the instructions available [here](https://accounts.snapchat.com/accounts/downloadmydata).
2. Once the upload is complete, extract the zip file and get the JSON file nammed `memories_history.json`.
3. Put the `memories_downloader.py` file in the same directory as the JSON file.
4. Place the Exiftool executable file in the same directory as the JSON file.
5. Open a command prompt in this directory and run the following command:
```bash
python memories_downloader.py
```

The script will then ask what is the name of the json file, leave empty if the file has not been renamed.

The script will download all your memories to a folder named `Snapchat Memories` located in the same directory as the `memories_downloader.py` file.

The metadata of each file will also be updated with the date and location of the photo or video.
