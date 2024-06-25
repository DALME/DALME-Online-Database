# Auth

When we talk about 'auth' there are two distinct components to that category
that need to be distinguished. There is some conceptual overlap between the two
but the distinction will continually manifest itself throughout our
architecture and solutions so it's worth making the difference clear from the
outset.

1. Authentication
2. Authorization

Where authentication is the process of verifying an identity (usually a user
but not always, it might be a machine we need to authenticate) and where
authorization is the process of determining if some actor should be permitted
to perform some action in some system or on a given resource.

Clearly we can't have one without the other but actually authorization is the
more general category. If we squint, we can imagine fairly easily how
authentication can be modelled within an authorization domain. That is to say,
authentication is that subset of authorization that deals with the secure and
correct identification of some given **identity** (an actor, which is just
another resource) and in doing so permits further authorization patterns to be
granted to that identity and the universe of resources it owns or controls,
once it has been confirmed as that owning identity.

That said, authentication must come **prior** to any kind of authorization
process as we cannot authorize an actor to do anything at all (short of letting
them do anything they want) if we haven't first identified them. Authentication
should be seen as a particular **type** of authorization with its own special
domain of rules and objects which are worth further abstracting over.
Authentication is the doorway to authorization.

In OIDC, which we use as our authentication layer, this subset relationship
becomes quite explicit seeing that OIDC is an identity layer built on top of
OAuth 2.0 which, strictly speaking, is an authorization framework.

Another more significant difference is that authentication generally only needs
to happen once (within a given timeframe) whereas we find authorization
dispersed throughout all levels of our application architecture, invoked at
various different moments. For example, at the db level where it might
constrain the filtering of rows, at the API level where it might guard access
to resources, within the groups and permissions controlling a CMS, and so on.
This makes implementing good authorization patterns a much more complex and
ongoing task when taken over the long term.

## Sessions & Tokens

- We're running two layers of auth. Sessions and tokens.
- The authorization code view is login protected by django-oauth-toolkit.
- Wagtail uses sessions out of the box. Django admin too.
- As long as the token authorization flow is dependent on a session being
  present then we can run them both side-by-side without issue.

## Sessions

## Tokens (OAuth)

The token-driven auth flow is used to secure the API as exposed to the Vue SPA.
To view the API docs themselves you'll need to be logged into the Django
session but to actually manipulate the resources via REST the SPA needs to
interface with an OAuth 2.0 compliant authentication and authorization system.

### Creating an OAuth Application

#### OIDC/PKCE Authentication Code Flow

An OAuth 'public client' should be understood as some application that cannot
hold some credential securely. This includes native desktop apps and JavaScript
driven SPAs such as IDA. Given this criteria, when the IDA app requests
tokens from the authorization server it means that there are additional
security concerns raised by using the Authorization Code Flow alone that must
be taken into account when we design our authorization system. Namely, that the
source code of the SPA can be decompiled to reveal the OAuth server's **Client
Secret**. To mitigate this vulnerability OAuth 2.0 provides a modified version
of the Authorization Code Flow known as PKCE - Proof Key for Code Exchange -
pronounced 'pixie'. This enhanced flow of Authorization Code Flow + PKCE is
specified by the OpenID Connect (OIDC) identity layer.

"The basic idea behind PKCE is ensuring that the application that starts the
authentication flow is the same one that finishes it."

"The OAuth server doesn't know the difference between the legitimate app that
starts the flow in step one and the malicious app that redeems the
authorization code."

##### The Code Verifier

In order to function, the PKCE enhancement introduces a new secret called the
**Code Verifier** which is created by the calling application (our SPA) at
login time around which the flow pivots. This Code Verifier will be used in
place of the Client Secret to confirm and secure our identity with the
authorization server.

Given this Code Verifier, the SPA also creates a transformed (hashed) version
of the Code Verifier called the **Code Challenge**. The Code Challenge is
transmitted to the authorization server over HTTPS along with a request for a
one-time **Authorization Code**.

The authorization server stores the hashed Code Challenge for later
verification and redirects back to the app with an Authorization Code once the
user has authenticated themselves. In our case this is done with an email and
password pair stored in an `ida.User` record.

Done in this way, at this stage any attacker can only intercept the
Authorization Code from the response which they cannot exchange for an API
token without the original Code Verifier secret.

Once the SPA has an Authorization Code in its hands it can make a request to
exchange the code for API tokens, only now it sends the Code Verifier with that
request instead of a fixed secret (namely, the Client Secret which we know we
cannot securely expose to a public client).

Finally, the Authorization Server can hash the Code Verifier it has received
and compare it to the hashed Code Challenge it stored earlier in order to
validate our identity and start emitting API tokens in the form of **Identity
tokens**, **Access Tokens** and **Refresh Tokens**.

We have been **authenticated** and are now safely in the domain of
authorization which is governed by the Authorization Code Flow.

## Authorization Code Flow

## Glossary
