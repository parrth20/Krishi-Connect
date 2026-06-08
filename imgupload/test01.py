import os

import requests


def identify_plant(file_names):
    # PlantNet API endpoint
    url = "https://my-api.plantnet.org/v2/identify/all"

    api_key = os.getenv("PLANTNET_API_KEY", "2b10Bz5aV3mdnKlqL7ioP8Vie")

    files = []
    opened_files = []
    for img in file_names:
        image_file = open(img, 'rb')
        opened_files.append(image_file)
        files.append(('images', image_file))

    params = {
    "api-key": api_key,
    "lang": "en"
    }

    try:
        response = requests.post(url, files=files, params=params, timeout=15)

        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        return response.json()

    except Exception as e:
        return {
            "error": "PlantNet API request failed",
            "details": str(e)
        }
    finally:
        for image_file in opened_files:
            image_file.close()


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)


'''
Testing block (not used in Django)

if __name__ == '__main__':
    x = identify_plant(["../img/photo1.jpg"])

    for key, value in recursive_items(x):
        print(key, value)
'''
