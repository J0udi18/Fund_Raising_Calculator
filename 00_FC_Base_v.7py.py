# import libraries
import pandas
import math


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
            return "yes"
        elif response == "no" or response == "n":
            return "no"

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


# Gets expenses, returns lists which has
# The data frame and sub_total
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
        item_name = not_blank("Item name: ", "The component name")
        if item_name.lower() == "xxx":
            break

        # if we have fixed costs, the quantity is one
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

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    expense_frame = expense_frame.set_index('Item')

    # Find sub_total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (use currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for profit goal
        response = input("what is your profit goal (eg $500 or 50%) ")

        # check if first character us $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue


        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. ie {:.2f} dollars? ,"
                                 " y / n ".format(amount, amount))

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%? , "
                                  "y / n".format(amount))
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# rounding function
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


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
used_before = yes_no("Have you used the program before? ")
if used_before == "no":
    instructions()
if used_before == "yes":
    print("**** Program launched! ****")

# Get product name

product_name = not_blank("Product name: ",
                         "The product name can't be blank.")
how_many = num_check("How many items will you be producing? ",
                     "The number of item must be a whole "
                     "number more than zero", int)

print()
print("Please enter your variable costs below...")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]
variable_txt = pandas.DataFrame.to_string(variable_frame)

variable_heading = "===== Variable Costs ======"

print()
have_fixed = yes_no("Do you have fixed costs (y / n)? ")

if have_fixed == "yes":
    # Get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)

    fixed_heading = "===== Fixed Costs ======"

else:
    fixed_sub = 0
    fixed_txt = ""
    fixed_heading = ""

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculate total sales needed to reach goal
sales_needed = all_costs + profit_target
round_to = num_check("Round to nearest...? $", "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print("Selling Price (unrounded): ${:.2f}".format(selling_price))

recommended_price = round_up(selling_price, round_to)
print(f"\nRRP: ${recommended_price}\n")

# strings for printing...

heading = f"****** {product_name} ******"
variable_heading = f"=== Variable Costs ===="
variable_sub_txt = f"Variable Costs Subtotal: {variable_sub}"
fixed_txt_variable = f"=== Fixed Costs ===="
variable_profit_target_txt = f"==== Profit & Selling Advice ===="


profit_target_txt = f"Profit Target: ${profit_target}"
sales_needed_txt = f"Required Sales: ${sales_needed}"
recommended_price_txt = f"Recommended Price: ${recommended_price}"

# List holding stuff to print / write to file
to_write = [heading, variable_heading, variable_txt, variable_sub_txt,
            fixed_txt_variable, variable_profit_target_txt, sales_needed_txt,
            recommended_price_txt]

# Write to file
# Create file to hold data (add .txt extension)
file_name = "{}.txt".format(product_name)
with open(file_name, "w+") as text_file:
    # Heading
    for item in to_write:
        text_file.write(item)
        text_file.write("\n\n")

    # # Write product name
    # text_file.write("/n **** Product Name: {} *****\n\n".format(product_name))
    #
    # # Write variable costs

    # text_file.write("{}\n".format(variable_txt))
    # text_file.write("/a Variable Costs Subtotal: {}\n\n".format(currency(variable_sub)))
    #
    # if have_fixed == "yes":
    #     # Write fixed costs
    #     text_file.write("/n /n === Fixed Costs ====\n\n")
    #     text_file.write("{}\n".format(fixed_txt))
    #     text_file.write("/n /n Fixed Costs Subtotal: {}\n\n".format(currency(fixed_sub)))
    #
    # # Write profit target and sales needed
    # text_file.write("/n/n ==== Profit & Selling Advice ====\n\n")
    # text_file.write("Profit Target: ${:.2f}".format(profit_target))
    # text_file.write("Required Sales: ${:.2f}\n\n".format(sales_needed))
    #
    # # Write recommended price
    # text_file.write("/n ==== Recommended Price: ${:.2f} ====\n".format(recommended_price))

# Print Stuff
for item in to_write:
    print(item)
    print()

# Write success message
print("Data written to file successfully!")
