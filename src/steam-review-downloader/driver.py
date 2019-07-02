from random import shuffle
from SentimentNetwork import SentimentNetwork


def pretty_print_review_and_label(i):
    print(reviews[i][0] + "\t:\t" + reviews[i][1][:80] + "...")


reviews = []
pos_file = open('positiveReviews.txt', 'r', encoding='utf-8')
for review in pos_file:
    reviews.append(('positive', review))
pos_file.close()

neg_file = open('negativeReviews.txt', 'r', encoding='utf-8')
for review in neg_file:
    reviews.append(('negative', review))
neg_file.close()

shuffle(reviews)

new_reviews = []
labels = []
for review in reviews:
    new_reviews.append(review[1])
    labels.append(review[0])
reviews = new_reviews


mlp_full = SentimentNetwork(reviews[:-1000],labels[:-1000],min_count=0,polarity_cutoff=0,learning_rate=0.01)
mlp_full.train(reviews[:-1000],labels[:-1000])