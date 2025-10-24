# Order Price Calculator using a Function

def calculate_final_price(quantity, unit_price, tax_percentage):
    """
    Calculate the final price of an order after tax.

    Parameters:
        quantity (int): Number of items
        unit_price (float): Price per item
        tax_percentage (float): Tax rate in percent

    Returns:
        dict: Order summary with subtotal, tax, and final price
    """
    subtotal = quantity * unit_price
    tax_amount = (tax_percentage / 100) * subtotal
    final_price = subtotal + tax_amount

    return {
        "quantity": quantity,
        "unit_price": unit_price,
        "subtotal": subtotal,
        "tax_percentage": tax_percentage,
        "tax_amount": tax_amount,
        "final_price": final_price
    }


def run_order_calculator():
    """Interactive CLI wrapper for calculate_final_price"""
    quantity = int(input("Enter quantity: "))
    unit_price = float(input("Enter unit price (£): "))
    tax_percentage = float(input("Enter tax percentage (%): "))
    return calculate_final_price(quantity, unit_price, tax_percentage)


def main():  # pragma: no cover
    order = run_order_calculator()

    print("\n----- Order Summary -----")
    print(f"Quantity: {order['quantity']}")
    print(f"Unit Price: £{order['unit_price']:.2f}")
    print(f"Subtotal: £{order['subtotal']:.2f}")
    print(f"Tax ({order['tax_percentage']}%): £{order['tax_amount']:.2f}")
    print(f"Final Price: £{order['final_price']:.2f}")


if __name__ == "__main__":  # pragma: no cover
    main()

