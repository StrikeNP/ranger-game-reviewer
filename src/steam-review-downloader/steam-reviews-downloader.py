import json
import time

import requests

def get_cleaned_game_reviews(appID, num_reviews = 1000):
    '''
    Get steam reviews, stripped to the useful information
    An individual review is a string containing the review text

    :param appID: Steam ID of the game to get reviews for
    :param num_reviews: The number of negative/positive reviews to retrieve
        This will retrieve num_reviews of both pos and neg reviews, so a
        value of 1000 will return 1000 pos reviews and 1000 neg reviews,
        totalling to 2000 reviews.
    :return: tuple of (neg_reviews[], pos_reviews[])
    '''
    reviews_per_request = 100
    api_limit_sleep_time = 0.0

    neg_reviews = []
    pos_reviews = []

    # Get num_reviews negative reviews
    for offset in range(0,num_reviews, reviews_per_request):
        time.sleep(api_limit_sleep_time)
        review_set = get_raw_review_set(appID, offset=offset, review_type="negative")
        # print("len" + str(len(review_set["reviews"])))
        # print(review_set)
        #break early if request was not successful
        if review_set["success"] is not 1:
            print('invalid, skipping')
            return neg_reviews, pos_reviews
        # if len(review_set["reviews"]) < num_reviews:
        #     break
        # print(review_set)
        for review in review_set["reviews"]:
            if review not in neg_reviews:
                review_text = review["review"]
                neg_reviews.append(review_text)

    # Get num_reviews positive reviews
    for offset in range(0,num_reviews, reviews_per_request):
        time.sleep(api_limit_sleep_time)
        review_set = get_raw_review_set(appID, offset=offset, review_type="positive")
        # if len(review_set["reviews"]) < num_reviews:
        #     break
        for review in review_set["reviews"]:
            if review not in pos_reviews:
                review_text = review["review"]
                pos_reviews.append(review_text)

    return neg_reviews, pos_reviews

def get_raw_review_set(appID, offset=0, filter ="recent", review_type ="all", num_reviews = 100):
    '''
    Get a set of 20 steam-reviews using the steam api. See documentation
    here: https://partner.steamgames.com/doc/store/getreviews

    :param appID: the ID of the game to get reviews for. Takes str or int
    :param offset: Reviews are returned in bundles of 20,
    this should be some multiple of 20 to prevent getting
    the same reviews over and over.
    :param filter: How to sort the returned reviews. Doc snipped from steam below
        "recent" : sorted by creation time
        "updated" : sorted by last updated time
        "all" : (default) sorted by helpfulness, with sliding windows based on day_range parameter,
            will always find results to return.
    :param review_type: The type of reviews to retrieve.
        "all" : all reviews
        "positive" : positive reviews
        "negative" : negative reviews
    :param num_reviews: The number of reviews to return (max 100)
    :return: A JSON object containing the review data for 20 reviews
    '''

    URL = "https://store.steampowered.com/appreviews/" + \
          str(appID) + "?json=1" + \
          "&start_offset=" + str(offset) + \
          "&filter=" + filter + \
          "&num_per_page=" + str(num_reviews) + \
          "&review_type=" + str(review_type) + \
          "#language=en"
    # print(URL)
    review_request = requests.get(url=URL)
    review_json = review_request.json()
    return review_json

def create_review_files(appID, num_reviews = 1000):
    '''
    Create two text files named negative_reviews_appID.txt and
    positive_reviews_appID.txt that contain newline seperated
    reviews of the given game.

    :param appID: Steam ID of the app to get reviews for
    :param num_reviews: The number of reviews per file
    :return:
    '''
    neg_reviews, pos_reviews = get_cleaned_game_reviews(appID, num_reviews=num_reviews)

    if len(neg_reviews) is not 0:
        neg_reviews_file = open("C:/Users/nchie/Documents/SteamReviews/negative/"+str(appID)+".txt","w+", encoding='utf-8')
    if len(pos_reviews) is not 0:
        pos_reviews_file = open("C:/Users/nchie/Documents/SteamReviews/positive/"+str(appID)+".txt","w+", encoding='utf-8')
    for review in neg_reviews:
        review = review.replace('\n', ' ').replace('\r', '')
        neg_reviews_file.write(review + "\n")

    for review in pos_reviews:
        review = review.replace('\n', ' ').replace('\r', '')
        pos_reviews_file.write(review + "\n")
    # neg_reviews_file.close()
    # pos_reviews_file.close()

steamAppIDs = []
with open("C:\\Users\\nchie\\ranger_game_reviewer\\src\\steam-review-downloader\\steamIDs.txt", encoding='utf-8') as idsFile:
    steamAppIDs = [line.rstrip('\n') for line in idsFile]

line = 3968
for appID in steamAppIDs[line:]:
    print("Getting reviews for " + str(appID) + "  | app " + str(line) + "/" + str(len(steamAppIDs)))
    create_review_files(appID, num_reviews=1000)
    line += 1
