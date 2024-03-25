import random


# Checks that user has entered yes / no to a question
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# displays instructions, returns 'None'
def instructions():
    print("**** Instructions ****")
    print()

    print("This program will ask you for....")
    print("- The name of the product you are selling")
    print("- How many items you plan on selling")
    print("- The costs for each component of the product")
    print("- How much money you want to make")
    print()

    print("It will then output an itemised list of the costs")
    print("with subtotals for the variable and fixed costs.")
    print("Finally it will tell you how much you should sell")
    print("each item for to reach your profit goal.")

    print("The data will also be written to a text file which "
          "has the same name as your product.")
    return ""


#  ***** Main Routines starts here *****
print("***** Welcome to the Fund Raising Calculator *****")
print()
played_before = yes_no("Have you played the game before? ")
if played_before == "no":
    instructions()
if played_before == "yes":
    print("**** Program launched! ****")
