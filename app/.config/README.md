# app/.config

Files the app reads at runtime in development and CI.

They live under `app/` because the dev container mounts `./app` at `/opt/app`,
and the CI image copies `./app` in, so both reach them with nothing extra. A
file bind-mounted on its own inside that mount is unreliable: Docker leaves an
empty placeholder at the mount point, and a long-running container can see the
placeholder instead of the file.

- **oidc.key**: the RSA private key django-oauth-toolkit signs OIDC tokens with
  in development and CI. It is not a secret, any more than the development
  database password is. Staging and production read their key from
  `OIDC_RSA_PRIVATE_KEY`, which ECS fills from Secrets Manager.
