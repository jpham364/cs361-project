# Jonathan Pham
# CS361 - Microservice for Zhi's project

# https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/
# This is for file checking


import os
import os.path

# This is for time sleeping
import time

# Infinitely run and trigger when a char.txt is created

print("Waiting for main program to request survey...")

while True:

    time.sleep(3)

    # Check if char.txt exists
    charPath = "char.txt"
    check_file = os.path.isfile(charPath)

    # If char.txt exists...
    while (check_file == True):

        repeatCheck = "char.txt"
        check_file = os.path.isfile(charPath)

        if check_file == False:
            continue
       
        # Open the file and then get the character inside the file
        charFile = open("char.txt", "r")
        character = charFile.read()

        currSum = 0

        print("Key: 1: No, 2: Not really, 3: Not sure, 4: Yeah kinda, 5: Yup")

        for i in range(5):
            
            if i == 0:
                if character == "Sora":
                    print("\nSora: First Question!")
                    answer = input("Is your problem something you have a hard time talking to others about? -- ")
                    currSum += int(answer)

            if i == 1:
                if character == "Sora":
                    print("\nSora: Second Question!")
                    answer = input("Are you having a hard time focusing on things you enjoy, such as your hobbies? -- ")
                    currSum += int(answer)

            if i == 2:
                if character == "Sora":
                    print("\nSora: Third Question!")
                    answer = input("Does this issue also affect those around you? It must be worrying -- ")
                    currSum += int(answer)


            if i == 3:
                if character == "Sora":
                    print("\nSora: Fourth Question!")
                    answer = input("Would the people close to you consider this problem more significant than you yourself believe? -- ")
                    currSum += int(answer)

            if i == 4:
                if character == "Sora":
                    print("\nSora: Fifth Question!")
                    answer = input("Have you ever considered taking drastic measures in hopes of getting rid of the issue? -- ")
                    currSum += int(answer)


        print(currSum)

        resultFile = open("result.txt", "w")
        resultFile.write(str(currSum))
        resultFile.close()

        charPath = "char.txt"
        check_file_stall = os.path.isfile(charPath)

        print("Finished your survey! Please return by pressing Enter in the main program...")
        while check_file_stall == True:
            charPath = "char.txt"
            check_file_stall = os.path.isfile(charPath)


        print("\nWaiting for main program to request survey...")
        break
        





    


    



