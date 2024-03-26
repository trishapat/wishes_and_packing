from file_handler import FileHandler

end_programme = False

operation_file_handler = FileHandler(
    path_history=r"history.json",
    path_balance_and_warehouse=r"balance_and_warehouse.json"
)


balance, warehouse = operation_file_handler.data_get_balance_and_warehouse()
operations = operation_file_handler.data_get_history()


print("Welcome to Sweet Dream")
while not end_programme:
    operation = input(f"Select an option:\n1. Deposit or withdraw\n2. Sell\n3. Buy"
                      f"\n4. Show account balance\n5. List out the products\n"
                      f"6. Warehouse\n7. Overview\n8. End\n")

    if operation == "1":
        withdraw_deposit = int(input("Provide the amount you want to withdraw or deposit: "))
        type = int(input("Choose option:\n1. withdraw\n2. deposit\n"))
        if type == 1:
            if balance >= withdraw_deposit:
                balance -= withdraw_deposit
                operations.append(f"You have withdrawn {withdraw_deposit} EUR")
                operation_file_handler.data_append_to_history(f"You have withdrawn {withdraw_deposit} EUR")
                print(f"You have withdrawn {withdraw_deposit} EUR")
            else:
                print(f"You can't withdraw. Your balance is: {balance} ")
        elif type == 2:
            balance += withdraw_deposit
            operations.append(f"You have deposited {withdraw_deposit} EUR")
            operation_file_handler.data_append_to_history(f"You have deposited {withdraw_deposit} EUR")
            print(f"You have deposited {withdraw_deposit} EUR")
        else:
            print("Choose correct option")

    if operation == "2":
        name = input("Enter product's name: ")
        amount = int(input("How much do you want to sell? "))
        product_found = False
        if amount < 0:
            print("You can't choose values below 0")
        else:
            for product in warehouse:
                if product.get("name") == name:
                    product_found = True
                    if product.get("quantity") >= amount:
                        product_sold = True
                        product["quantity"] -= amount
                        balance += amount * product["price"]
                        print("You have sold a product.")
                        operations.append(f"You have sold {name} in: {amount} quantity")
                        operation_file_handler.data_append_to_history(f"You have sold {name} in: {amount} quantity")
                    else:
                        print(f"We are sorry. Product in stock: {product["quantity"]} ")
                        product_sold = False
            if not product_found:
                print("We are sorry. We don't have such a product in our assortment.")

    if operation == "3":
        name = input("Enter product's name: ")
        price = float(input("Enter product's price: "))
        quantity = int(input("Enter the quantity of ordered products: "))
        if price < 0 or quantity < 0:
            print("You can't choose values below 0")
        else:
            if balance >= price * quantity:
                warehouse.append({
                    "name": name,
                    "price": price,
                    "quantity": quantity
                })
                balance = balance - (price * quantity)
                operations.append(f"You have bought {name} in {quantity} quantity for {price} EUR each")
                operation_file_handler.data_append_to_history(f"You have bought {name} in {quantity} quantity for {price} EUR each")
                print(f"You have bought {name} in {quantity} quantity for {price} EUR each")
            else:
                print(f"We are sorry, but you can't buy these items. "
                      f"Your balance is: {balance}")

    if operation == "4":
        print(f"Your balance is: {balance} EUR")

    if operation == "5":
        print(warehouse)

    if operation == "6":
        name = input("Enter product's name: ")
        product_found = False
        for product in warehouse:
            if product.get("name") == name:
                product_found = True
                print("Product details:")
                print(f"Name: {product['name']}")
                print(f"Price: {product['price']} EUR")
                print(f"Quantity in stock: {product['quantity']}")
        if not product_found:
            print("Product not found in the warehouse.")

    if operation == "7":
        if not operations:
            print("No operations to show.")
        else:
            start_input = input("Enter the initial range (leave empty to start from the beginning): ")
            finish_input = input("Enter the final range (leave empty to end at the last index): ")
            start = int(start_input) if start_input else 0
            finish = int(finish_input) if finish_input else len(operations)
            invalid_input = False
            try:
                if start < 0 or finish > len(operations) or start >= finish:
                    invalid_input = True
                    print("Invalid range. Please enter valid indexes.")
                else:
                    for index, op in enumerate(operations[start:finish], start=start):
                        print(f"{index}: {op}")
            except ValueError:
                invalid_input = True
                print("Invalid input. Please enter valid indexes.")
            if invalid_input:
                print("Valid range: ")
                for index in range(len(operations)):
                    print(index)

    if operation == "8":
        end_programme = True
        operation_file_handler.data_save_balance_and_warehouse(balance=balance, warehouse=warehouse)
