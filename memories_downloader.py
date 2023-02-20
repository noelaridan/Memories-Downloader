import json
import requests
import os
import time

# Request the name of the json file
filepath = input("Enter the name of the JSON file [memories_history.json]: ")
if not filepath:
    filepath = "memories_history.json"

# Check if the file exists
if not os.path.exists(filepath):
    print("The {} file does not exist.".format(filepath))
    exit()

# Load data from the json file
with open(filepath, 'r') as f:
    data = json.load(f)

# Check if the Snapchat Memories folder exists
if not os.path.exists("Snapchat Memories"):
    # If the file does not exist, create it
    os.mkdir("Snapchat Memories")

# Counter to track the number of files downloaded
counter = 1
total = len(data['Saved Media'])

# Loop to download each memory
for memory in data['Saved Media']:
    date = memory['Date']
    media_type = memory['Media Type']
    location = memory['Location']
    download_link = memory['Download Link']
    
    # Extract the year from the date
    year = date[:4]
    # Extract the month from the date
    month = date[5:7]
    # Extract the day from the date
    day = date[8:10]

    # Define the file name according to date and media type
    if media_type == 'Video':
        filepath = os.path.join(os.getcwd(), "Snapchat Memories", "{}-{}-{} ({})".format(year, month, day, counter) + '.mp4')
        filename = "{}-{}-{} ({})".format(year, month, day, counter) + '.mp4'
    else:
        filepath = os.path.join(os.getcwd(), "Snapchat Memories", "{}-{}-{} ({})".format(year, month, day, counter) + '.jpeg')
        filename = "{}-{}-{} ({})".format(year, month, day, counter) + '.jpeg'
    
    # POST request on the first URL
    first_request = requests.post(download_link)
    if first_request.status_code != 200:
        print("POST request error: {}\nError code: {} \n".format(download_link, first_request.status_code))
    else :
        # Download the file
        response = requests.get(first_request.content)
        if response.status_code != 200:
            print("File download error: {}\nError code: {} \n".format(download_link, response.status_code))
        else:
            open(filepath, 'wb').write(response.content)

            real_media_type = os.popen('.\exiftool -FileType "' + filepath + '"').read().split(":")[1].strip()

            # If the media type is video, check if the file is a video
            if media_type == 'Video' and real_media_type != 'MP4':
                print("Warning: {} is not a video.".format(filename))
                media_type = 'Image'

                # Rename the file
                old_filepath = filepath
                filepath = filepath[:-4] + '.jpeg'
                filename = filename[:-4] + '.jpeg'

                # If the file already exists, replace it
                if os.path.exists(filepath):
                    os.remove(filepath)
                os.rename(old_filepath, filepath)
            # If the media type is image, check if the file is an image
            elif media_type == 'Image' and real_media_type != 'JPEG':
                print("Warning: {} is not an image.".format(filename))
                media_type = 'Video'

                # Rename the file
                old_filepath = filepath
                filepath = filepath[:-4] + '.mp4'
                filename = filename[:-4] + '.mp4'

                # If the file already exists, replace it
                if os.path.exists(filepath):
                    os.remove(filepath)
                os.rename(old_filepath, filepath)
            
            # Define the metadata for the file
            if media_type == 'Video':
                # If location is not available, do not add metadata
                if location == 'Latitude, Longitude: 0.0, 0.0':
                    os.popen('.\exiftool -overwrite_original -QuickTime:CreateDate="' + date + '" "' + filepath + '"').read()
                else:
                    os.popen('.\exiftool -overwrite_original -QuickTime:CreateDate="' + date + '" -GPSLatitude="' + location.split(': ')[1].split(', ')[0] + '" -GPSLongitude="' + location.split(': ')[1].split(', ')[1] + '" "' + filepath + '"').read()
            else:
                # If location is not available, do not add metadata
                if location == 'Latitude, Longitude: 0.0, 0.0':
                    os.popen('.\exiftool -overwrite_original -DateTimeOriginal="' + date + '" "' + filepath + '"').read()
                else:
                    os.popen('.\exiftool -overwrite_original -DateTimeOriginal="' + date + '" -GPSLatitude="' + location.split(': ')[1].split(', ')[0] + '" -GPSLongitude="' + location.split(': ')[1].split(', ')[1] + '" "' + filepath + '"').read()

            # Changes the creation and modification date of the file
            timestamp = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S UTC'))
            os.utime(filepath, (timestamp, timestamp))

            # Display the status and percentage of downloads
            print("[{}/{}] Download of {} is completed. ({}%)".format(counter, total, filename, round(counter / total * 100), 2))

    # Increment the counter
    counter += 1
