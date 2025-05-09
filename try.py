def divide_numbers():
    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        result = num1 / num2  # This may cause ZeroDivisionError
        print(f"Result: {result}")
    except ZeroDivisionError:
        print("Error: You cannot divide by zero!")
    except ValueError:
        print("Error: Please enter valid numbers.")
    else:
        print("Division successful!")
    finally:
        print("Thank you for using the calculator.")

# Run the function
divide_numbers()