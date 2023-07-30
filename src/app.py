import discord_bot
import asyncio

import email_access
import order_parser

email = email_access.get_order()
print(f"Store: {email['sender']}")
print(f"Time: {email['date']}")
order = order_parser.parse_order(email_access.get_order()['body'])
order_parser.print_order(order)
print(f"Multiplier: {order['total']/order['subtotal']:.3f}")

async def check_for_email():
    email_dict = {'email_body': ''}
    while True:
        if(is_new_email(email_dict)):
            order = email_parse(email_dict['email_body'])
            if(is_shared_order(order)):
                share_order(order)
        asyncio.sleep(60)

async def main():
    await asyncio.gather(
        check_for_email()
        #Discord function 2
        #Discord function 3
    )

asyncio.run(main())