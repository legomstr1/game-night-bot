# Game Night Bot

This is an open source discord bot.
### Currently Functionality:
- Food Order Payments
    - Importing a **GrubHub** email from **Gmail**
    - Parsing the order and extracting the items and costs
    - Calculating actual costs after delivery fee, tip, and tax
    - Posting in **Discord** the items listed on the order, requesting 'reactions' from users based on their order
    - Issuing **Venmo** requests to users based on a *prefilled* csv file containing discord username and venmo username connections

### Planned Functionality:
- *Food Order Payments*
    - Importing a **Doordash**, **UberEats**, or **GrubHub** email from **Gmail** or **Outlook**
    - Payment requests
        - From **Venmo**, **PayPal**, or **Cash** based on a stored individual user preference
        - Automatic username request and storage