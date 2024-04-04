import pandas

# Frames and content for export

variable_dict = {
    "Item": ["Mugs", "Printing", "Packaging"] ,
    "Quantity": [300, 300, 50],
    "Price": [1, .5, .75]
}

fixed_dict = {
    "Item": ["Rent", "Artwork", "Advertising"],
    "Price": [25, 35, 10]
}

variable_frame = pandas.DataFrame(variable_dict)
fixed_frame = pandas.DataFrame(fixed_dict)

# Change frames to strings
variable_txt = pandas.DataFrame.to_string(variable_frame)
fixed_txt = pandas.DataFrame.to_string(fixed_frame)

product_name = "Custom Mugs"
profit_target = "Profit Target: $100.00"
required_sales = "Total Sales: $200.00"
Minimum_price = "Minimum price: $2.88"
recommended_price = "The recommended price: $5.00"

# List holding stuff to print / write to file
to_write = [product_name, variable_txt, fixed_txt,
            profit_target, required_sales,
            recommended_price]


# Write to file
# Create file to hold data (add .txt extension)
file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")

# Heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# Print Stuff
for item in to_write:
    print(item)
    print()