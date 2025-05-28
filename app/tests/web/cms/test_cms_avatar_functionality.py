"""Test basic avatar functionality in the CMS."""

import pytest

from django.conf import settings
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_avatar_saving_user(auth_user, avatar_image):
    auth_user.avatar.save(avatar_image.name, avatar_image, save=True)

    assert (
        auth_user.avatar.url
        == f'/{settings.MEDIA_LOCATION}/public/{settings.AVATARS_LOCATION}/user/{avatar_image.name}'
    )


@pytest.mark.django_db
def test_avatar_saving_teammember(team_member, avatar_image):
    team_member.avatar.save(avatar_image.name, avatar_image, save=True)

    assert (
        team_member.avatar.url
        == f'/{settings.MEDIA_LOCATION}/public/{settings.AVATARS_LOCATION}/teammember/{avatar_image.name}'
    )


@pytest.mark.django_db
def test_avatar_url_retrieval(team_member, avatar_image):
    user = team_member.user
    # Because the property `avatar_url` favours a team_member avatar over a user
    # avatar, the following assertion only works if the avatar is set in the `user` model first
    user.avatar.save(avatar_image.name, avatar_image, save=True)
    assert (
        team_member.avatar_url
        == f'/{settings.MEDIA_LOCATION}/public/{settings.AVATARS_LOCATION}/user/{avatar_image.name}'
    )

    # If the team member avatar is set, it should now override the user's avatar
    team_member.avatar.save(avatar_image.name, avatar_image, save=True)
    assert (
        team_member.avatar_url
        == f'/{settings.MEDIA_LOCATION}/public/{settings.AVATARS_LOCATION}/teammember/{avatar_image.name}'
    )


@pytest.mark.django_db
@pytest.mark.urls('app.urls.urls_tenant')
def test_avatar_rendering_in_views(superuser, avatar_image, test_username, test_password, test_domain):
    client = Client(HTTP_HOST=test_domain.domain)
    client.login(username=test_username, password=test_password)
    response = client.get(reverse('wagtailadmin_home'))

    assert '<img src="//www.gravatar.com/avatar' in response.content.decode(response.charset)

    superuser.avatar.save(avatar_image.name, avatar_image, save=True)

    response = client.get(reverse('wagtailadmin_home'))
    assert (
        f'<img src="/{settings.MEDIA_LOCATION}/public/{settings.AVATARS_LOCATION}/user/{avatar_image.name}"'
        in response.content.decode(response.charset)
    )
