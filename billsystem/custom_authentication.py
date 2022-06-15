def custom_user_authentication_rule(user):
    """
    Override the default user authentication rule for Simple JWT Token to return true if there is a user and let
    serializer check whether user is active or not to return an appropriate error.
Add 'USER_AUTHENTICATION_RULE': 'path_to_custom_user_authentication_rule' to simplejwt settings to override the default.
    :param user: user to be authenticated
    :return: True if user is not None
    """

    return True if user is not None else False