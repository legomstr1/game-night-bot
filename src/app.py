import discord_bot
import asyncio

import email_handler
import order_parser

email = email_handler.get_order()
print(f"Store: {email['sender']}")
print(f"Time: {email['date']}")
order = order_parser.parse_order(email_handler.get_order()['body'])
order_parser.print_order(order)
print(f"Multiplier: {order['total']/order['subtotal']:.3f}")

async def check_for_email():
    email = {'date': ''}
    while True:
        is_new, email = email_handler.is_new_order(email)
        if is_new:
            order = order_parser.email_to_order(email)
            if(discord_bot.is_shared_order(order)):
                discord_bot.share_order(order)
        asyncio.sleep(60)

async def main():
    await asyncio.gather(
        check_for_email()
        #Discord function 2
        #Discord function 3
    )

asyncio.run(main())