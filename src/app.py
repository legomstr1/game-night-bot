import email_access
import order_parser

email = email_access.get_order()
print(f"Store: {email['sender']}")
print(f"Time: {email['date']}")
order_parser.print_order(order_parser.parse_order(email_access.get_order()['body']))
