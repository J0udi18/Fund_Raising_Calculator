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
    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    item_name = ""
    while item_name.lower() != "xxx":
        print()
        item_name = not_blank("Item name: ", "The component name")
        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            quantity = num_check("Quantity:", "The amount must be a whole number", int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $", "The price must be a number < more than 0", float)

        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)

    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']
    expense_frame = expense_frame.set_index('Item')

    sub_total = expense_frame['Cost'].sum()

    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Print expense frames
def expense_print(heading, frame, subtotal):
    print()
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))
    return ""


def profit_goal(total_costs):
    error = "Please enter a valid profit goal\n"
    valid = False
    while not valid:
        response = input("what is your profit goal (eg $500 or 50%) ")
        if response[0] == "$":
            profit_type = "$"
            amount = response[1:]
        elif response[-1] == "%":
            profit_type = "%"
            amount = response[:-1]
        else:
            profit_type = "unknown"
            amount = response
        try:
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue
        except ValueError:
            print(error)
            continue
        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. ie {:.2f} dollars? , y / n ".format(amount, amount))
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"
        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%? , y / n".format(amount))
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"
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
    print("The data will also be written to a text file which has the same name as your product.")
    return ""


def main():
    print("***** Welcome to the Fund Raising Calculator *****")
    print()
    played_before = yes_no("Have you used the program before? ")
    if played_before == "no":
        instructions()
    if played_before == "yes":
        print("**** Program launched! ****")
        input("Press Enter to exit...")

    product_name = not_blank("Product name: ", "The product name can't be blank.")
    how_many = num_check("How many items will you be producing? ", "The number of item must be a whole number more "
                                                                   "than zero", int)

    print()
    print("Please enter your variable costs below...")
    variable_expenses = get_expenses("variable")
    variable_frame = variable_expenses[0]
    variable_sub = variable_expenses[1]

    print()
    have_fixed = yes_no("Do you have fixed costs (y / n)? ")

    if have_fixed == "yes":
        fixed_expenses = get_expenses("fixed")
        fixed_frame = fixed_expenses[0]
        fixed_sub = fixed_expenses[1]
    else:
        fixed_sub = 0
        fixed_frame = ""

    all_costs = variable_sub + fixed_sub
    profit_target = profit_goal(all_costs)

    sales_needed = all_costs + profit_target
    round_to = num_check("Round to nearest...? $", "Can't be 0", int)

    selling_price = sales_needed / how_many
    print("Selling Price (unrounded): ${:.2f}".format(selling_price))

    recommended_price = round_up(selling_price, round_to)
    print(f"\nRRP: ${recommended_price}\n")

    variable_dict = {
        "Item": variable_expenses[0].index.tolist(),
        "Quantity": variable_expenses[0]["Quantity"].tolist(),
        "Price": variable_expenses[0]["Price"].tolist()
    }

    fixed_dict = {
        "Item": fixed_frame.index.tolist(),
        "Price": fixed_frame["Cost"].tolist()
    }

    print("Writing data to file...")
    with open(f"{product_name}.txt", "w+") as text_file:
        text_file.write("**** Fund Raising - {} ******\n\n".format(product_name))
        # Write other data to the file
        text_file.write("Variable Costs:\n")
        text_file.write(str(variable_expenses[0]))
        text_file.write("\n\nFixed Costs:\n")
        text_file.write(str(fixed_frame))
        # Write other sections
    print("Data written to file successfully!")
