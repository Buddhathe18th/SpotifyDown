import music_tag
import requests


def get_image(song):
    f=music_tag.load_file("Songs\\Perfect.mp3")
    img_data = requests.get(song["image_url"]).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    with open('image_name.jpg', 'rb') as img_in:
        f['artwork'] = img_in.read()
    f.save()

