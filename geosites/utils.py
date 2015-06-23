# we could create a wrapper around the get_current_site here to return wither the site or no sites or *all if we are in the master site.

def resolve_object(user, model, query, site, permission='base.view_resourcebase'):
    """This resolve object should be site aware.
        We should not pass any http request objects to it, but the view should pass the request.user instead."""
    pass