import pandas


# checks user has entered an integer
def num_check(question, error, num_type):
    while True:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


# Checks that user has entered yes / no to a question
def yes_no(question):
    while True:

        response = input(question).lower()

        if response == "yes" or response == "y":
            return response
        elif response == "no" or response == "n":
            return response
        else:
            print("Please enter either yes or no...\n")


# checks that ticket name is not blank
def not_blank(question, error):
    valid = False

    while not valid:
        response = input(question)

        # If name is not blank, program continues
        if response == "":
            print("{}. \nplease try again.\n".format(error))
            continue

        return response


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# Get expenses, returns list which has
# the data frame and sub_total
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("Item name: ", "The component name can't be blank.")
        if item_name.lower() == "xxx":
            break

        quantity = num_check("Quantity:",
                             "The amount must be more than zero",
                             int)
        price = num_check("How much for a single item? $",
                          "The price must be a number < more than 0",
                          float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame

    # Find sub_total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (use currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency())

    return [expense_frame, sub_total]


# Print expense frames
def expense_print(heading, frame, subtotal):
    print()
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))
    return ""


# *** Main routine strats here ***

# Get product name
product_name = not_blank("product name: ", "The product name")

print()
print("Please enter your variable costs below...")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()
have_fixed = yes_no("Do you have fixed costs (y / n)? ")

if have_fixed == "yes":
    # Get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
else:
    fixed_sub = 0
    fixed_frame = ""

# Find Total Costs

# Ask user for profit goal

# Calculate recommended price

# Write data to file

# **** Printing Area ****

print("**** Variable costs ****")
print(variable_frame)
print()

print("Variable costs: ${:.2f}".format(variable_sub))

print("**** Fixed Costs *****")
print(fixed_frame[['Cost']])
print()
print("Fixed costs: ${:.2f}",format(fixed_sub))

print()
print("***** Fun Raising - {} *****".format(product_name))
print()
expense_print("Variable", variable_frame, variable_sub)

if have_fixed == "yes":
    expense_print("Fixed", fixed_frame, variable_sub)
# Set up dictionaries and lists
