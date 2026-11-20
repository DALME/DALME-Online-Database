# tf/CLAUDE.md

Infrastructure guidance. The root `CLAUDE.md` holds the project-wide rules,
gates and commands, and `.github/CLAUDE.md` the deploy workflow.

## Layout

Terragrunt over Terraform modules. `root.hcl` is the shared root,
`environments/staging` is the one live environment, `nodes/` holds one unit per
part of the stack, and `modules/` holds `infra`, `services` and `_reusable`.
`environments/production` holds only a README.

## Working here

- Everything runs in the `ida.deploy` container through make:
  `make deploy.plan module=<name>`, `make deploy.lint`, and the rest of the
  `deploy.*` targets.
- Staging is the only environment Terraform manages. Production runs v1
  (`master`) on a separate stack outside Terraform, and is out of scope.
- Never apply. Plans are for review, and an apply is a deploy, which is jhrr's
  to run.
- The ECS start chain in `modules/services/ida/main.tf` runs management
  commands on every deploy. Changing one changes every deploy.

Tool and pattern choices (Terragrunt or Terramate, OpenTofu or Terraform) wait
on ADRs under #62.
