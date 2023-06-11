"""
1. Set a check every 5 minutes for new food order emails or instantly check when a message is received from the host.
2. Message the host and ask whether the order is a group order, and then wait for a reaction.
3. If the reaction indicates that the order is not a group order, terminate the process.
4. If the reaction confirms that it is a group order, continue the process.
5. Parse the order and send it to the main channel, then wait for user reactions.
6. After receiving a reaction, verify if the user has a stored Venmo username.
7. If a Venmo username exists for the user, create a Venmo request for the number of items they reacted to and send it to the user's Venmo account.
8. If the user doesn't have a stored Venmo username, send a message in Discord to ask for their Venmo username.
9. Validate the Venmo username provided by the user. If it's not valid, ask for it again. If it's valid, store it for future use.
10. Once the Venmo username is stored, proceed to send a Venmo request as described in step 7.
"""