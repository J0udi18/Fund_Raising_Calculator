import pandas


# checks user has entered an integer
def num_check(question, error, num_type):
    while True:

        try:
            response = int(input(question))
            return response

        except ValueError:
            print("Please enter an integer")


# checks that ticket name is not blank
def not_blank(question, error):
    valid = False

    while not valid:
        response = input(question)

        # If name is not blank, program continues
        if response != "":
            print("{}. \nplease try again.\n".format(error))
            continue

        return response


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)

# Get expenses, returns list which has
# the data frame and sub total
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    global quantity
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
        item_name = not_blank("Item name: ",
                              "The component name can't be blank")
        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            quantity = num_check("Quantity:",
                             "The amount must be a whole number",
                             int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $",
                          "The price must be a number < more than 0",
                          float)

        # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')



# *** Main routine strats here ***

# Get product name
product_name = not_blank("product name: ", "The product name")

fixed_expenses = get_expenses("fixed")


variable_expenses = get_expenses("fixed")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# *** Printing Area ***

print()
print(fixed_frame[['Cost']])
print()

print("Fixed Costs: ${:.2f}".format(fixed_sub))
# Set up dictionaries and lists

item_list = []
quantity_list = []
price_list = []

variable_dict = {
    "Item": item_list,
    "Quantity": quantity_list,
    "Price": price_list
}

# Get user data
product_name = not_blank("product name: ",
                         "The product name can't be blank.")

# loop to get component, quantity and price
item_name = ""
while item_name.lower() != "xxx":

    print()
    # get name, quantity and item
    item_name = not_blank("Item name: ",
                          "The component name can't be"
                          "blank.")
    if item_name.lower() == "xxx":
        break

    quantity = num_check("Quantity:",
                         "The amount must be a whole number "
                         "more than zero",
                         int)
    price = num_check("How much for a single item? $",
                      "The price must be a number <more "
                      "than 0>",
                      float)

    # add item, quantity and price to lists
    item_list.append(item_name)
    quantity_list.append(quantity)
    price_list.append(price)

variable_frame = pandas.DataFrame(variable_dict)
variable_frame = variable_frame.set_index('Item')

# Calculate cost of each component
expense_frame['Cost'] = expense_frame['Quantity'] * expense


# Calculate cost of each component
variable_frame['cost'] = variable_frame['Quantity'] \
                         * variable_frame['Price']
# Find sub total
variable_sub = variable_frame['cost'].sum()

# Currency Formatting (uses currency function)
add_dollars = ['Price', 'Cost']
for item in add_dollars:
    variable_frame[item] = variable_frame[item].apply(currency)

return [expese frame, sub total]

# *** Printing Area ***

price(variable_frame)

print()

print("Variable Costs: ${:.2f}".format(variable_sub))
