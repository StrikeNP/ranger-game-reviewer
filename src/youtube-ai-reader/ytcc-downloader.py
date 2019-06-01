from ytcc.download import Download

video_id = '_un8mHYFJp0'
download = Download()
# Language is optional and default to "en"
# YouTube uses "en","fr" not "en-US", "fr-FR"
captions = download.get_captions(video_id, 'en')

review_file = open("review.txt","w+")
review_file.write(captions)
# print(captions)
