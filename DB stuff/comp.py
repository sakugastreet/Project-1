scriplist = [
    "1 And now it came to pass that there was a great multitude gathered together, of the people of Nephi, round about the temple which was in the land Bountiful; and they were marveling and wondering one with another, and showing one to another the great and marvelous change which had taken place.",
    "2 And they were also conversing about this Jesus Christ, of whom the sign had been given concerning his death.",
    "3 And it came to pass that while they were thus conversing one with another, they heard a voice as if it came out of heaven; and they cast their eyes round about, for they understood not the voice which they heard; and it was not a harsh voice, neither was it a loud voice; nevertheless, and notwithstanding it being a small voice it did pierce them that did hear to the center, insomuch that there was no part of their frame that it did no tcause to quake; yea, it did pierce them to the very soul, and did cause their hearts to burn."
]


def CompareString(string0, string1):
    if string0 == string1:
        return True
    
    else:
        return False

def main():
    while (True):

        print("hello!")
        print("which verse would you like to practice")
        print("1")
        print("2")
        print("3")

        UserChoice = int(input(""))
        if UserChoice == 0:
            break
        while (True):
            userInput = input(f"Please enter verse {UserChoice}: ")
            if userInput == "0":
                break
            elif CompareString(userInput, scriplist[UserChoice - 1]) == True:
                break
            else:
                output = ""
                for char in userInput:
                    if char == scriplist[UserChoice - 1]:
                        output += char
                    else:
                        output += "*"

                


                print("Sorry, that's incorrect.")
                print(output)
                input("press enter to contiue")
                

    


main()