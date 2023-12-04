# Auth

When we talk about 'auth' there are two distinct components to that category
that should be distinguished. There is some overlap between the two but the
distinction will manifest itself throughout our architecture and solutions so
it's worth making the difference clear from the outset.

1. Authentication
2. Authorization

Where authentication is the process of verifying an identity (usually a user
but not always, it might be a machine we need to authenticate), and where
authorization is the process of determining if some actor should be permitted
to perform some action in some system or on a given resource.

Clearly we can't have one without the other but actually authorization is the
more general category. If we squint, we can imagine fairly easily how
authentication can be modelled within an authorization domain. That is to say,
authentication is that subset of authorization that deals with the secure and
correct identification of some given **identity** (an actor, which is just
another resource), and so permitting further authorization patterns to be
granted to that identity and the universe of resources it owns or controls,
once it has been confirmed as that owning identity.

That said, authentication must come **prior** to any kind of authorization
process as we cannot authorize an actor to do anything at all (short of letting
them do anything they want) if we haven't first identified them. Authentication
should be seen as a privileged type of authorization with its own special
domain of rules and objects which are worth further abstracting over.
Authentication is the doorway to authorization.

In OIDC, which we use as our authentication layer, this subset relationship is
quite explicit seeing that OIDC is an identity layer built on top of OAuth 2.0
which, strictly speaking, is an authorization framework.

Another more significant difference is that authentication generally only needs
to happen once (within a given timeframe) whereas we find authorization
dispersed throughout all levels of our application architecture and happening
all the time. For example, at the db level where it might constrain filtering,
at the API level where it might guard access to resources, within the groups
and permissions of a CMS, and so on. This makes implementing good authorization
patterns a more complex and ongoing task over the long term.
