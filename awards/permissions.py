def can_create_award(user, return_error_msg=False):
    """
    Return True if requesting user can create an Award object.

    Normal users do not have this permission. Only users with permission of
    `awards.add_award` may create matches.

    By default all admin users have this permission.
    """
    has_perms = user.has_perm('awards.add_award')
    error_msg = 'Only service accounts can create matches.'

    if not has_perms:
        if return_error_msg:
            return False, error_msg
        else:
            return False

    else:
        if return_error_msg:
            return True, error_msg
        else:
            return True
