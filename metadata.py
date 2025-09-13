import music_tag

song=music_tag.load_file("Songs\Ed Sheeran - Perfect [Official Lyric Video].mp3")
song.remove_tag('title')
song.append_tag('title', 'Perfect')
song.save()

print(song)