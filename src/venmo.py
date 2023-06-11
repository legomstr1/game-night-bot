from venmo_api import Client
import configparser
from pathlib import Path

def request_money(username: str, amount: float) -> bool:
    """
    This function sends a request to a specific Venmo user for money.

    Parameters:
    username (str): The username of the Venmo user.
    amount (float): The amount to be requested.

    Returns:
    bool: True if the request was successful, False otherwise.
    """
    # Create a configparser object
    config = configparser.ConfigParser()

    # Formulate the path to the config file
    config_path = Path(__file__).resolve().parent.parent / 'api_keys.config'
    
    # Read the configuration file
    config.read(config_path)

    # Get the access token
    venmo_access_token = config.get('DEFAULT', 'venmo_access_token')
    
    # Creating a Venmo client using the access token from the config module
    venmo = Client(access_token=venmo_access_token)

    # Getting the user object from Venmo for the given username
    user = venmo.user.get_user_by_username(username)

    # Checking if the user object is not None (user exists)
    if user is not None:
        # Sending a request to the user for money
        # Assuming request_money returns a boolean indicating success
        success = venmo.payment.request_money(amount, "test request", target_user=user)
        return success
    else:
        print(f"User {username} not found.")
        return False
    
def is_valid_username(username: str) -> bool:
    pass