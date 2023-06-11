import email_access
import order_parser

order_parser.print_order(order_parser.parse_order(email_access.get_order()['body']))
