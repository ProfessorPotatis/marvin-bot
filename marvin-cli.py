#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example to show how command-line options can be handled by a script.
"""



import sys
import os
from datetime import datetime
import getopt



#
# Add some stuff about this script
#
PROGRAM = os.path.basename(sys.argv[0])
AUTHOR = "Sofia Kristiansen"
EMAIL = "sofiakristiansen@gmail.com"
VERSION = "1.0"
USAGE = """{program} - Bernard the all-knowing whale. By {author} ({email}), version {version}.

Usage:
  {program} [options] command [arguments-to-the-command]

Options:
  -h --help                      Display this help message.
  -v --version                   Print version and exit.
  --verbose                      Verbose mode.
  -s --silent                    Do not display any details or statistics about the execution.
  --output                       Sets output file.
  --input                        Sets input file.
  --json                         Activate json functions.

Arguments:
  ping
        Pings a webpage.
        Can be used as follows:
                            ping <url>

  ping-history
        Shows the content in the textfile 'history.txt'
        Can be used as follows:
                            ping-history

  get
        Gets the content of a webpage.
        Can be used as follows:
                            get <url>
                            --output=<file> get <url>

  quote
        Gives you a random 'quote of the day'.
        Can be used as follows:
                            quote
                            --input=<file> quote

  title
        Gets the title of a choosen webpage.
        Can be used as follows:
                            title <url>
                            --input=<file> title

  seo
        Gets and analyses a webpage out of a
        search engine optimisation perspective.
        Can be used as follows:
                            seo <url>
                            --json seo <url>
                            --input=<file> seo
                            --json --input=<file> seo


""".format(program=PROGRAM, author=AUTHOR, email=EMAIL, version=VERSION)

MSG_VERSION = "{program} version {version}.".format(program=PROGRAM, version=VERSION)
MSG_USAGE = "Use {program} --help to get usage.\n".format(program=PROGRAM)




#
# Global default settings affecting behaviour of script in several places
#
REPEAT = 0
SILENT = False
VERBOSE = True
NAME = ""
PING = False
HISTORY = False
GET = False
OUTPUT = None
QUOTE = False
INPUT = None
TITLE = False
SEO = False
JSON = False

EXIT_SUCCESS = 0
EXIT_USAGE = 1
EXIT_FAILED = 2



def printUsage(exitStatus):
    """
    Print usage information about the script and exit.
    """
    print(USAGE)
    sys.exit(exitStatus)



def printVersion():
    """
    Print version information and exit.
    """
    print(MSG_VERSION)
    sys.exit(EXIT_SUCCESS)



def pingWebpage():
    """
    Example of how to ping a webpage for a status code, basically just
    to check that the page is there and the webserver is replying with
    a positive code, such as 200.
    Then writes down and saves the ping in the textfile 'history.txt'.
    """

    import time
    import requests

    url = NAME

    try:
        # Get current time
        rTime = time.ctime(time.time())

        # Request header from url
        print("Ready to send HTTP request to", url, "\n(press return)", end='')
        input()
        req = requests.head(url)

        # Print result
        if VERBOSE == True:
            print("Request to ", url, " sent at ", rTime)

        print("Recieved status code: ", req.status_code)

        # Save result to file
        with open("history.txt", 'a') as history:
            history.write("Request to " + url + " sent at " + rTime + " Recieved status code: " \
            + str(req.status_code) + "\n")

    except requests.ConnectionError:
        print("Failed to connect")



def pingHistory():
    """
    Opens, reads and writes out the content of the file 'history.txt', which
    contain content that has been saved in the function 'pingWebpage'.
    """

    history = open("history.txt", 'r')
    print(history.read())



def getWebpage():
    """
    Gets/scrapes the webpages content and writes it out on the screen.
    """
    import requests

    # pip install beautifulsoup4
    from bs4 import BeautifulSoup

    input("Press enter to continue. ")

    # Get webpage
    url = NAME
    print("\nReady to send HTTP request to ", url, "\nPress enter to continue. ", end='')
    input()
    req = requests.get(url)
    print("\nThe response status code is:\n", req.status_code)

    # Get the webpage content as a soup
    soup = BeautifulSoup(req.text, "html.parser")
    title = soup.title
    if OUTPUT == None:
        print("The title of the webpage is:", title)
        print("\nThe content of the webpage:")
        print(soup.get_text())
    else:
        file = open(OUTPUT, 'w')
        file.write(soup.get_text())
        print("The content of the webpage has been saved and can be viewed in the file " + OUTPUT + ".")



def quote():
    """
    Get a random quote from a webservice and print it out.

    The webservice in the example is:
    http://dbwebb.se/javascript/lekplats/get-marvin-quotes-using-ajax/quote.php
    """

    import requests

    input("Press enter to continue. ")

    url = "http://dbwebb.se/javascript/lekplats/get-marvin-quotes-using-ajax/quote.php"

    try:
        if INPUT == None:
            print("\nReady to send HTTP request to ", url, "\nPress enter to continue. ", end='')
            input()
            req = requests.get(url)

            print("\nThe response status code is:\n", req.status_code)

            print("\nThe response body is:\n", req.text)

            json = req.json()
            print("\nQuote of today is:\n{quote}\n".format(quote=json["quote"]))
        else:
            print("\nFetching JSON-object from choosen file.\n")
            import json
            import random

            listOfQuotes = []

            with open(INPUT) as fileObject:
                obj = json.load(fileObject)

            for quotes in obj["quotes"]:
                listOfQuotes.append(quotes)

            nr1 = len(listOfQuotes) - 1
            print("Quote of today is:\n" + listOfQuotes[random.randint(0, nr1)] + "\n")

    except requests.ConnectionError:

        print("Failed to connect.")



def getTitle():
    """
    Get and show the title of a choosen webpage.
    """
    import requests

    # pip install beautifulsoup4
    from bs4 import BeautifulSoup

    input("Press enter to continue. ")

    if INPUT == None:
        # Get webpage
        url = NAME
        print("\nReady to send HTTP request to", url, "\nPress enter to continue. ", end='')
        input()
        req = requests.get(url)
        print("\nThe response status code is:\n", req.status_code)

        # Get the webpage content as a soup
        soup = BeautifulSoup(req.text, "html.parser")
        title = soup.title.string

        print("The title of the webpage is:", title)
    else:
        webpage = open(INPUT, 'r').read()
        soup = BeautifulSoup(webpage, "html.parser")
        title = soup.title.string
        print("The title of the webpage is:", title)



def seo():
    """
    Gets and analyses a webpage out of a search engine optimisation perspective.
    Counts the number of <title> elements and the number of characters in the title-element.
    Counts the number of <h1> and <h2> elements.
    Counts the number of <a> elements.
    """
    import requests

    from bs4 import BeautifulSoup

    input("Press enter to continue. ")

    if INPUT == None:
        # Get webpage
        url = NAME
        print("\nReady to send HTTP request to ", url, "\nPress enter to continue. ", end='')
        input()
        req = requests.get(url)
        print("\nThe response status code is:\n", req.status_code)

        soup = BeautifulSoup(req.text, "html.parser")
        title = soup.title.string
        h1 = soup.find_all('h1')
        h2 = soup.find_all('h2')
        link = soup.find_all('a', href=True)

        if JSON == False:
            # Result
            print("\nTitle of the webpage: ", title)
            print("Number of characters in the title element: ", len(title))
            print("Number of <h1> elements: ", len(h1))
            print("Number of <h2> elements: ", len(h2))
            print("Number of <a> elements:: ", len(link))
        else:
            import json
            print("\nUsing JSON.")
            # Generate json file
            jtitle = title
            jlentitle = len(title)
            jh1 = len(h1)
            jh2 = len(h2)
            jlink = len(link)

            # Append the data as a dict to the data array
            jsonobject = {"SEO":[
                {"titleOfWebpage":jtitle},
                {"nrOfCharTitle":jlentitle},
                {"nrOfh1":jh1},
                {"nrOfh2":jh2},
                {"nrOfLinks":jlink}
            ]}
            print(jsonobject)

            # Open the file for writing ("w" will replace the file contents)
            jsonfile = open("jsonseo.txt", "w")

            # Encode json with pretty output (indent)
            json.dump(jsonobject, jsonfile, sort_keys=True, indent=4)


    else:
        pagedata = open(INPUT, "r").read()
        soup = BeautifulSoup(pagedata, "html.parser")
        title = soup.title.string
        h1 = soup.find_all('h1')
        h2 = soup.find_all('h2')
        link = soup.find_all('a', href=True)

        if JSON == False:
            # Result
            print("\nTitle of the webpage: ", title)
            print("Number of characters in the title element: ", len(title))
            print("Number of <h1> elements: ", len(h1))
            print("Number of <h2> elements: ", len(h2))
            print("Number of <a> elements:: ", len(link))
        else:
            import json
            print("\nUsing JSON.")
            # Generate json file
            jtitle = title
            jlentitle = len(title)
            jh1 = len(h1)
            jh2 = len(h2)
            jlink = len(link)

            # Append the data as a dict to the data array
            jsonobject = {"SEO":[
                {"titleOfWebpage":jtitle},
                {"nrOfCharTitle":jlentitle},
                {"nrOfh1":jh1},
                {"nrOfh2":jh2},
                {"nrOfLinks":jlink}
            ]}
            print(jsonobject)

            # Open the file for writing ("w" will replace the file contents)
            jsonfile = open("jsonseo.txt", "w")

            # Encode json with pretty output (indent)
            json.dump(jsonobject, jsonfile, sort_keys=True, indent=4)



def parseOptions():
    """
    Merge default options with incoming options and arguments and return them as a dictionary.
    """

    # Switch through all options
    try:
        global VERBOSE, PING, NAME, HISTORY, GET, OUTPUT, QUOTE, INPUT, TITLE, SEO, JSON

        opts, args = getopt.getopt(sys.argv[1:], "hvvso:i:j", [
            "help",
            "version",
            "verbose",
            "silent",
            "output=",
            "input=",
            "json"
        ])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                printUsage(EXIT_SUCCESS)

            elif opt in ("-v", "--version"):
                printVersion()

            elif opt in ("--verbose"):
                VERBOSE = True

            elif opt in ("-s", "--silent"):
                VERBOSE = False

            elif opt in ("--output"):
                OUTPUT = arg

            elif opt in ("--input"):
                INPUT = arg

            elif opt in ("--json"):
                JSON = True

            else:
                assert False, "Unhandled option"



        if args[0] in "ping":
            PING = True
            NAME = args[1]

        if args[0] in "ping-history":
            HISTORY = True

        if args[0] in "get":
            GET = True
            NAME = args[1]

        if args[0] in "quote":
            QUOTE = True
            NAME = args[0]

        if args[0] in "title":
            TITLE = True
            if len(args) > 1:
                NAME = args[1]

        if args[0] in "seo":
            SEO = True
            if len(args) > 1:
                NAME = args[1]

        if len(args) == 0:
            assert False, "Missing argument"


    except Exception as err:
        print(err)
        print(MSG_USAGE)
        # Prints the callstack, good for debugging, comment out for production
        #traceback.print_exception(Exception, err, None)
        sys.exit(EXIT_USAGE)




def main():
    """
    Main function to carry out the work.
    """
    startTime = datetime.now()

    parseOptions()

    if PING == True:
        pingWebpage()

    if HISTORY == True:
        pingHistory()

    if GET == True:
        getWebpage()

    if QUOTE == True:
        quote()

    if TITLE == True:
        getTitle()

    if SEO == True:
        seo()

    timediff = datetime.now()-startTime
    if VERBOSE:
        sys.stderr.write("Script executed in {}.{} seconds\n".format(timediff.seconds, timediff.microseconds))

    sys.exit(EXIT_SUCCESS)



if __name__ == "__main__":
    main()
