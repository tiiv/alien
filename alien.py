#!/usr/bin/python

import httplib
import json
import sys
import time

if (len(sys.argv) != 2):
    print "Invalid number of arguments.\n"
    print "Usage: alien <subreddit>\n"
    sys.exit(0)

try:
    # establish connection
    connection = httplib.HTTPConnection("www.reddit.com")

    # send request
    method = "GET"
    path = "/r/%s/hot.json" % sys.argv[1]
    body = None
    header = {"User-Agent": "Alien 0.1 by /u/tiiv"}
    connection.request(method, path, body, header)

    # fetch response
    response = connection.getresponse()
    
    # parse json data
    data = json.loads(response.read())

    # fetch current utc time
    current_utc = time.time() - time.timezone

    # print header
    print
    print "25 Hottest submissions of \033[0;34m/r/%s" % (sys.argv[1])
    print

    # print submission infos
    for submission in iter(data["data"]["children"]):

        # submission attributes
        attributes = submission["data"]

        # parse time of submission
        submitted = current_utc - attributes["created_utc"]
        unit = "minute"
        if (submitted > 60 * 60 * 24):
            submitted = round(submitted / 60 / 60 / 24)
            unit = "day"
        elif (submitted > 60 * 60):
            submitted = round(submitted / 60 / 60)
            unit = "hour"
        elif (submitted > 60):
            submitted = round(submitted / 60)

        # append 's' if plural 
        if (submitted >= 2):
            unit += "s"

        # print info
        info  = "\033[1;36m"
        info += "%5d" % attributes["score"]
        info += "   "
        info += "\033[1;37m"
        info += "\"%s\"" % attributes["title"]
        info += "\033[1;30m"
        info += "\n"
        info += "        -- submitted %d %s by %s\n" % (submitted, unit, attributes["author"]) 
        print info

except httplib.HTTPException:
    print "Unable to reach Reddit's server."
