import music_tag
import requests
import os

from Backend.spotipyMain import sanitize


def tag_music(song):
    try:

        file=music_tag.load_file("Songs/"+song["playlist"]+"/"+str(sanitize(song["name"]))+" - "+str(song["artists"])+".mp3")
    except Exception as e:
        print("Tagging failed for:"+str(song["name"]))
        print(e)
        with open("skipped.txt", "a", encoding="utf-8") as f:
                f.write(str(song)+"\n")
        return
    file["title"]=song["name"]

    for artist in song["artists"]:
        file["artist"]=str(file["artist"])+artist+";"
    file["artist"]=str(file["artist"])[:-1]
    file["album"]=song["album"]

    img_data = requests.get(song["image_url"]).content
    with open('temp_image.jpg', 'wb') as img:
        img.write(img_data)
    with open('temp_image.jpg', 'rb') as img:
        file['artwork'] = img.read()

    os.remove("temp_image.jpg")

    file.save()
