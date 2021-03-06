#!/usr/bin/env python3
import twitter
import os
import time
import creds
import math
import random

FLAME_DIR = "flames"

api = twitter.Api(consumer_key=creds.consumer_key,
                  consumer_secret=creds.consumer_secret,
                  access_token_key=creds.access_token_key,
                  access_token_secret=creds.access_token_secret)

# Post an image and return the id
def postImage(img, tweetA=None, tweetB=None):
    bodyText = ""
    if tweetA and tweetB:
        def url(x): return api.GetStatus(int(x)).urls[0]
        bodyText = "Generated from {} and {}".format(url(tweetA), url(tweetB))
    return api.PostUpdate(bodyText, img).id

# Get the score of an image, given its tweet ID
def getImageScore(imgId):
    s = api.GetStatus(int(imgId))
    cr = s.created_at_in_seconds
    score = s.favorite_count + s.retweet_count
    timeUp = math.ceil((time.time() - cr) / 386400) # Days up
    return score/timeUp

# Gets the filenames of two tweets to use
def getTweets():
    tids = []

    for x in os.listdir(FLAME_DIR):
        if x.endswith(".flam3"):
            tids.append(x[:-len(".flam3")])

    tids = sorted(tids, key=getImageScore)
    
    # Organised. Pick two

    index = round(math.log2(random.randint(0, 2 ** (len(tids) - 1))))

    a = tids[index]

    index = round(math.log2(random.randint(0, 2 ** (len(tids) - 1))))

    b = tids[index]

    apath = os.path.join(FLAME_DIR, a + ".flam3")
    bpath = os.path.join(FLAME_DIR, b + ".flam3")

    return apath, bpath

if __name__=='__main__':
    import sys
    ret = {
        "post": postImage,
        "popular": getTweets,
    }[sys.argv[1]](*sys.argv[2:])
    if isinstance(ret, tuple):
        for x in ret: print(x, end="\0")
    else:
        print(ret)
