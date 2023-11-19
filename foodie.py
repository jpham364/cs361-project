
# used this resource to help hide my API Key
# https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c
import config

# Using Google Maps Python Client on Github
# https://github.com/googlemaps/google-maps-services-python
import googlemaps

# Conncect with API key 
gmaps = googlemaps.Client(key=config.apiKey)


# This function takes a zipCode and a keyword string as a parameter
# This function uses the Google Maps API to first take the zipcode that the user enters
# And then converts it to Lat/Long coordinates in order to use the Nearby Search function
# The function will return a JSON object that we can use to extract names of places
def processList(zipCode, keyword):
 
    # Using this geocode function in order to get the JSON object to get the latitude and longitude 
    geocode_result = gmaps.geocode(zipCode)

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    long = geocode_result[0]["geometry"]["location"]["lng"]
    
    # for the places.nearby() function to work, the location has to be in a string.
    #  So we are combining the lat/long into a string separated by a comma. 
    location = str(lat) + "," + str(long)

    # Checks for places nearby within 10km
    places = gmaps.places_nearby(location, 10000, keyword)
    
    # Return JSON object 
    return places
  

# This function takes in a zip code and then checks if the length of the input is 5
# In addition, it will check if the input are all digits
# Returns a boolean value false if not a valid zip code
def zipCodeCheck(zipCode):
    if(len(zipCode) != 5):
        return False
    if(zipCode.isdigit() == False):
        return False
    return True

# This function enters the keyword input page for the user
# The user can type keywords, which will be added to a list
# Once the user decides to finish adding keywords, the funciton will 
# convert the list objects and converts it into a string to be processed as a keyword 
# for the processList() function.
def keywordMode(keyWordString):

    # Initialize list
    keywordList = []

    print("\nYou entered keyword mode! Commands below:")
    print("Enter any word to input keywords")
    print("'e' to exit keyboard input")
    print("'li' to see list of keywords")
    print("'u' to undo your last filter keyword")

    # Make an infinite loop for users to continuously add keywords until exit
    while True:
        keywordInput = input("User Input -- ")
        
        # When the user exists
        if keywordInput == 'e':

            # Concatenate keyWordString to be returned 
            for i in keywordList:
                keyWordString = keyWordString + ", " + i
            print("Exited Keyword mode")
            break

        # When the user undos a keyword
        elif keywordInput == 'u':
            
            # This makes sure that nothing bad happens if you pop an empty list
            if len(keywordList) == 0:
                continue 
            else:
                keywordList.pop()

        # When the users wants to see the list of current keywords
        elif keywordInput == 'li':
            print(keywordList)

            # If no commands are put, everything else is a keyword
        else:
            keywordList.append(keywordInput)
                
    return keyWordString

def genPlanmode(zipCode): 
    print("\nYou entered planning mode!")

    numPlaces = None
    planKeywords = []

    # This double checks for number input 
    while True: 
        numPlaces = input("Enter how places you would like to visit (MAX 5): ")
        if numPlaces.isdigit() == False:
            continue
        if (int(numPlaces) <= 5) & (int(numPlaces) > 0):
            break

    # This loop will ask the user for a keyword for each place
    for i in range(int(numPlaces)):
        print("\nPlace " + str(i + 1) + "...")
        currKeyword = input("What are you feeling? (enter keyword): ")
        planKeywords.append(currKeyword)

    # For each keyword inputted, it will process a list to be appended to a text file starting from 1-5
    for i in range(int(numPlaces)):
        currList = processList(zipCode, planKeywords[i])
        createPath = "planner/" + str(i+1) + ".txt"
        currString = ""

        for j in currList["results"]:
            currString = currString + (j["name"]) + "~"

        # https://www.w3schools.com/python/ref_string_rstrip.asp
        # This is to remove the trailing comma 
        currString = currString + str(numPlaces)

        f = open(createPath, "w")
        f.write(currString)
        f.close()
            
    



if __name__ == "__main__":
    print("Welcome to Foodie!")

    # Automatic keyword for restaurant to dial in places
    keywords = "Restaurant"

    # While loop to check for valid zip code
    while True:
        zipCode = input("Please enter a zip code: ")
        zipCheck = zipCodeCheck(zipCode)
        if zipCheck == True:
            break
        else:
            print("Please try again!\n")
    
    while True:
        print("\nList:")
        
        currList = processList(zipCode, keywords)

        # Print the list of places found
        for i in currList["results"]:
                print(i["name"])

        # Available commands for now
        print("\nEnter 'k' to enter new keywords to filter results")
        print("Enter 'p' to generate a plan for the day!")
        print("Enter 'x' to exit program")

        # Make this program go indefinitely, but there will be an exit condition for the user
        # which is pressing x
        listInput = input("User Input -- ")

        # Enters keyword mode, clears any exisiting keyword to reset
        if listInput == 'k':
            keywords = "Restaurant"
            keywords = keywordMode(keywords)

        elif listInput == 'p':
            genPlanmode(zipCode)

        # Exit
        elif listInput == 'x':
            print("\nThanks for using Foodie!")
            exit()

        else:
            print("\nError input! Try again")
            






