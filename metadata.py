import music_tag


def tag_music(song):
    file=music_tag.load_file("Songs\\"+str(song["name"])+".mp3")

    file["title"]=song["name"]

    for artist in song["artists"]:
        file["artist"]=str(file["artist"])+artist+";"
    file["artist"]=str(file["artist"])[:-1]
    file["album"]=song["album"]

    file.save()
