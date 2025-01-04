{ pkgs, lib, config, inputs, ... }:

{
 packages= [ pkgs.git ];
  languages.python.enable = true;
  languages.python.uv.enable = true;
  languages.python.uv.sync.enable = true;
  languages.python.uv.sync.allExtras = true;
  languages.python.venv.enable = true;
  #
  enterShell = ''
    hello
    git --version
  '';

  # https://devenv.sh/tasks/
 scripts.pytest.exec = ''
    pytest
  '';
  # tasks = {
  #     "myproj:"
    # "myproj:setup".exec = "mytool build";
    # "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  pre-commit = {
      hooks = {
          ruff.enable = true;
          ruff-format.enable = true;

      };
  };
  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
    pytest
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
