{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [
      pkgs.git
      pkgs.act
  ];
  languages.python.enable = true;
  languages.python.uv.enable = true;
  languages.python.uv.sync.enable = true;
  languages.python.uv.sync.allExtras = true;
  languages.python.venv.enable = true;

  scripts.build.exec = ''
      uv build
  '';

  pre-commit = {
    hooks = {
      # mypy.enable = true;
      ruff.enable = true;
      ruff-format.enable = true;
    };
  };
  enterTest = ''
    act --graph
  '';
}
