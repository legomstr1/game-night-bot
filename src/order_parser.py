import re
from lxml import html


def parse_order(html_string: str):
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

    # Extract subtotal, service fee, sales tax, tip, and total charge using XPath
    subtotal = root.xpath('//td[contains(text(), "Items subtotal")]/following-sibling::td/text()')
    subtotal = float(subtotal[0].replace("$", ""))
    service_fee = root.xpath('//td[contains(text(), "Service fee")]/following-sibling::td/text()')
    service_fee = float(service_fee[0].replace("$", ""))
    sales_tax = root.xpath('//td[contains(text(), "Sales tax")]/following-sibling::td/text()')
    sales_tax = float(sales_tax[0].replace("$", ""))
    tip = root.xpath('//td[contains(text(), "Tip")]/following-sibling::td/text()')
    tip = float(tip[0].replace("$", ""))
    total_charge = root.xpath('//td[contains(text(), "Total charge")]/following-sibling::td/b/text()')
    total_charge = float(total_charge[0].replace("$", ""))

    # Prepare the final order dictionary
    order = {
        'items': items_ordered,
        'subtotal': subtotal,
        'fee': service_fee,
        'tax': sales_tax,
        'tip': tip,
        'total': total_charge
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
