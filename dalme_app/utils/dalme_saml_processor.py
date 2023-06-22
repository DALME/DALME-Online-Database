from djangosaml2idp.processors import BaseProcessor


class SAMLProcessor(BaseProcessor):
    """Subclasses the default djangosaml2idp processor to allow for special fields to be included in response."""

    def create_identity(self, user, sp_attribute_mapping: dict[str, str]) -> dict[str, str]:
        """Add extra fields to the response."""
        results = {}
        for user_attr, out_attr in sp_attribute_mapping.items():
            attr_lst = user_attr.split('.')
            if len(attr_lst) > 1 and attr_lst[0] == 'profile':
                results[out_attr] = getattr(user.profile, attr_lst[1])
            if user_attr == 'groups':
                results[out_attr] = list(user.groups.values_list('name', flat=True))
            # elif user_attr == 'profile_image':
            #     results[out_attr] = user.profile.profile_image
            elif hasattr(user, user_attr):
                attr = getattr(user, user_attr)
                results[out_attr] = attr() if callable(attr) else attr
        return results
