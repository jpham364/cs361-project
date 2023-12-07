
# https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c
# Used to get api key inside of config.py
import config

# https://github.com/googlemaps/google-maps-services-python
import googlemaps

# https://pypi.org/project/colorama/
from colorama import Fore

import time,os

gmaps = googlemaps.Client(key=config.apiKey)

# The function will return a JSON object that we can use to extract names of places
def processList(zipCode, keyword):
 
    # Geocode function to get the JSON object & convert to string
    geocode_result = gmaps.geocode(zipCode)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    long = geocode_result[0]["geometry"]["location"]["lng"]
    
    location = str(lat) + "," + str(long)

    places = gmaps.places_nearby(location, 10000, keyword) # 10km radius
    
    return places
  
def zipCodeCheck(zipCode):
    if(len(zipCode) != 5):
        return False
    if(zipCode.isdigit() == False):
        return False
    return True

def keywordPrint():
    print("\nYou entered keyword mode! Commands below:")
    print("Enter any word to input keywords")
    print("'e' to exit keyboard input")
    print("'li' to see list of keywords")
    print("'u' to undo your last filter keyword")

# Note: Cannot split else ifs in this function 
def keywordMode(keyWordString):
    keywordList = []
    keywordPrint()

    while True:
        keywordInput = input("User Input -- ")
        
        if keywordInput == 'e':     # Exits

            # Convert keywordList into keywordString to be returned for the processList() function.
            for keyword in keywordList:
                keyWordString = keyWordString + ", " + keyword
            print("Exited Keyword mode")
            break

        # When the user undos a keyword, has error handling if you pop an empty list
        elif keywordInput == 'u':
            
            if len(keywordList) == 0:
                continue 
            else:
                keywordList.pop()

        elif keywordInput == 'li':      # List of current keywords
            print(keywordList)

        else:
            keywordList.append(keywordInput) # Everything else is a keyword
                
    return keyWordString

# Check input between 1-5
def checkNumInput():
    numPlaces = 0
    while True: 
        numPlaces = input("Enter how places you would like to visit (MAX 5): ")
        if numPlaces.isdigit() == False:
            continue
        if (int(numPlaces) <= 5) & (int(numPlaces) > 0): 
            break
    return numPlaces

# Creates keyword list to be processed by API
def keywordCreate(numPlaces, planKeywords):
    for place in range(int(numPlaces)):
        print("\nPlace " + str(place + 1) + "...")
        currKeyword = input("What are you feeling? (enter keyword): ")

        currKeyword = "Restaurant," + currKeyword
        planKeywords.append(currKeyword)
    return planKeywords

# Adds list of restaurants in x.txt files inside of planner directory
def processPlannerFiles(numPlaces, planKeywords, zipCode):

    for place in range(int(numPlaces)):
        currList = processList(zipCode, planKeywords[place])
        createPath = "planner/" + str(place+1) + ".txt"
        currString = ""

        for entry in currList["results"]:
            currString = currString + (entry["name"]) + "~"

        # https://www.w3schools.com/python/ref_string_rstrip.asp
        # This is to remove the trailing comma 
        currString = currString + str(numPlaces)

        # For each file in the planner, write the list of locations
        planner = open(createPath, "w")
        planner.write(currString)
        planner.close()

def createRequest():
    request = open("request.txt", "w")
    request.write("")
    request.close()

def genPlanmode(zipCode): 
    print("\nYou entered planning mode!")

    numPlaces = None
    planKeywords = []

    numPlaces = checkNumInput()

    # Ask the user for a keyword for each place they want to visit, insert in planKeywords list
    keywordCreate(numPlaces, planKeywords)

    # For each keyword inputted, it will process a list to be appended to a text file starting from 1-5.txt
    processPlannerFiles(numPlaces, planKeywords, zipCode)

    createRequest()
    return int(numPlaces)

def printPlan(numPlaces):
    print("Here is your generated plan!\n ")
    for planI in range(numPlaces):
        
        header = str(planI + 1) + ". "
        place = planResult.readline()
        place = place.rstrip('\n')
        print(header + place)




if __name__ == "__main__":

    # https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
    print(Fore.MAGENTA + """                                      
                                                   ,---. 
            ,------.                ,--.,--.       |   | 
            |  .---',---.  ,---.  ,-|  |`--' ,---. |  .' 
            |  `--,| .-. || .-. |' .-. |,--.| .-. :|  |  
            |  |`  ' '-' '' '-' '\ `-' ||  |\   --.`--'  
            `--'    `---'  `---'  `---' `--' `----'.--.  
                                                   '--'
          """)

    # Automatic keyword for restaurant to dial in places
    keywords = "Restaurant"

    # Check for valid zip code
    while True:
        zipCode = input(Fore.WHITE + "Please enter a zip code: ")
        zipCheck = zipCodeCheck(zipCode)
        if zipCheck == True:
            break
        else:
            print("Please try again!\n")
    
    # User input loops indefinitely, will print restaurant list every loop
    while True:
        print("\nList:")
        
        currList = processList(zipCode, keywords)

        for i in currList["results"]:
                print(Fore.WHITE + i["name"])

        print("\nEnter 'k' to enter new keywords to filter results")
        print("Enter 'p' to generate a plan for the day!")
        print("Enter 'x' to exit program")

        listInput = input("User Input -- ")

        # Enters keyword mode, clears any exisiting keyword to reset
        if listInput == 'k':
            keywords = "Restaurant"
            keywords = keywordMode(keywords)

        # Enters planning mode
        elif listInput == 'p':

            numPlaces = genPlanmode(zipCode)

            time.sleep(4)
            planResult = open("output.txt", "r")
            
            printPlan(numPlaces)
            
            input("\nPress enter to continue")
            os.remove("request.txt")

        # Exits program
        elif listInput == 'x':
            print("\nThanks for using Foodie!")
            exit()

        else:
            print("\nError input! Try again")
            