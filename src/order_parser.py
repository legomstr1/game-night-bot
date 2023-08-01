import re
from lxml import html

def extract_amount(root, label):
    """
    Extract a dollar amount related to a particular label from an HTML tree.

    Parameters:
    root (lxml.html.HtmlElement): The root of the HTML tree.
    label (str): The label of the value to extract.

    Returns:
    float: The extracted dollar amount, or None if not found.
    """
    
    # Create the XPath query string.
    xpath_query = f'//td[contains(text(), "{label}")]/following-sibling::td//text()'

    # Execute the XPath query.
    text_results = root.xpath(xpath_query)

    # Iterate over the results.
    for text in text_results:
        # If a dollar sign is found, this is the correct text.
        if "$" in text:
            # Remove the dollar sign and whitespace, then convert to float.
            amount = text.replace("$", "").strip()
            return float(amount)

    # If no text contained a dollar sign, return None.
    return None

def email_to_order(email:dict) -> dict:
    if email['sender'] == "Grubhub <orders@eat.grubhub.com>":
        return parse_grubhub(email['body'])
def parse_grubhub(html_string: str) -> dict:
    """
    Function to parse an HTML string containing order details.
    It extracts items ordered, their quantities, names, and prices.
    Also, it collects details like subtotal, service fee, sales tax, tip, and total charge.

    :param html_string: str, HTML string containing order details
    :return: dict, order details
    """
    # Convert the HTML string into an HTML element tree
    root = html.fromstring(html_string)

    # Extract the item elements using XPath
    items_elements = root.xpath('//table//table//table//table//table//tr')

    # Initialize list to store parsed items
    items_ordered = []

    for item in items_elements:
        # Extract item details using XPath
        quantity = item.xpath('.//td[1]/span/text()')
        name = item.xpath('.//td[2]/span/text()')
        price_text = item.xpath('.//td[3]//text()')

        # Check if quantity, name, and price_text are all available
        if quantity and name and price_text:
            detail = [subitem.strip(' •\xa0') for subitem in name[1:] if subitem.strip(' •\xa0')]
            name = name[0].strip()
            quantity = int(quantity[0].strip())
            price_text = ' '.join(price_text)

            # Extract price using regular expression
            price = float(re.search(r'\$(\d+(\.\d{2})?)', price_text).group(1))

            # Store the item details in items_ordered list
            items_ordered.append({
                'quantity': quantity,
                'name': name,
                'detail': detail,
                'price': price,
            })

    labels = ["Items subtotal", "Service fee", "Sales tax", "Tip", "Total charge"]
    # Use a dictionary comprehension to store the results in a dictionary
    # Keyed by the label for easy access.
    amounts = {label: extract_amount(root, label) for label in labels}


    # Prepare the final order dictionary
    order = {
        'items': items_ordered,
        'subtotal': amounts['Items subtotal'],
        'fee': amounts['Service fee'],
        'tax': amounts['Sales tax'],
        'tip': amounts['Tip'],
        'total': amounts['Total charge']
    }

    return order

def print_order(order):
    """
    Function to print the order details in a structured format.

    :param order: dict, order details
    """
    print("\nOrder Details:\n")

    for idx, item in enumerate(order['items'], 1):
        print(f"Item {idx}:")
        print(f"  Name: {item['name']}")
        print(f"  Quantity: {item['quantity']}")
        print(f"  Price: ${item['price']:.2f}")
        
        # Check if 'detail' exists and is not empty
        if 'detail' in item and item['detail']:
            print(f"  Detail: {', '.join(item['detail'])}")
        else:
            print("  Detail: None")
        print()

    print(f"Subtotal: ${order['subtotal']:.2f}")
    print(f"Service Fee: ${order['fee']:.2f}")
    print(f"Sales Tax: ${order['tax']:.2f}")
    print(f"Tip: ${order['tip']:.2f}")
    print(f"Total Charge: ${order['total']:.2f}")


##################################################################################
quantity = int(1)
name = str("rogan josh")
detail = ["mild, extra josh"]
price = float(8.60)

quantity2 = int(2)
name2 = str("lamb")
detail2 = ["spicy, hold the rogan"]
price2 = float(10.50)

# This dictionary represents an item in an order. 
# It includes information about the quantity ordered, the name of the item, any additional details, and the price of the item.


food = {
    'quantity': quantity,  # Int. The number of units of this item that were ordered.
    'name': name,  # String. The name of the item.
    'detail': detail,  # List of strings. Additional details about the item. For example, this might include specifications for a product, or special instructions for a food order.
    'price': price,  # Float. The price of a single unit of this item.
}

food2 = {
    'quantity': quantity2,  # Int. The number of units of this item that were ordered.
    'name': name2,  # String. The name of the item.
    'detail': detail2,  # List of strings. Additional details about the item. For example, this might include specifications for a product, or special instructions for a food order.
    'price': price2,  # Float. The price of a single unit of this item.
}

item = [food, food2 ]

subtotal = float(20.50)
service_fee = float(5.30)
sales_tax = float(8.80)
tip = float(10.20)
total_charge = float(100)

for_testing = {
    'items': item,  # A list of dictionaries, where each dictionary represents an item. See the 'item' dictionary below.
    'subtotal': subtotal,  # Float. The total cost of the items ordered before any fees, taxes, or tips.
    'fee': service_fee,  # Float. The service fee charged on the order.
    'tax': sales_tax,  # Float. The sales tax charged on the order.
    'tip': tip,  # Float. The tip given by the customer.
    'total': total_charge  # Float. The total charge to the customer, including items, fees, taxes, and tip.
}