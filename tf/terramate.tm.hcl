terramate {
  required_version = "~> 0.8.4"

  config {
    git {
      default_remote = "origin"
      default_branch = "ocp/development.v2"
    }
    run {
      env {
        TF_PLUGIN_CACHE_DIR = "$HOME/.terraform.d/plugin-cache"
      }
    }
  }
}
