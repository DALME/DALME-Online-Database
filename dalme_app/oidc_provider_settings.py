def userinfo(claims, user):
    # Populate claims dict.
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['given_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['email'] = user.email
    claims['address']['street_address'] = '...'
    claims['preferred_username'] = user.username
    return claims
