import email_access
import order_parser

email = email_access.get_order()
print(f"Store: {email['sender']}")
print(f"Time: {email['date']}")
order = order_parser.parse_order(email_access.get_order()['body'])
order_parser.print_order(order)
print(f"Multiplier: {order['total']/order['subtotal']:.3f}")
