{
  description = "Development environment for devto.py";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    nix-github-actions.url = "github:nix-community/nix-github-actions";
    devenv = {
      url = "github:cachix/devenv";
    };
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
    };
  };

  outputs = {
    self,
    nixpkgs,
    devenv,
    flake-parts,
    nix-github-actions,
    ...
  } @ inputs:
    flake-parts.lib.mkFlake {inherit inputs;}
    {
      imports = [
        inputs.devenv.flakeModule
      ];
      systems = nixpkgs.lib.systems.flakeExposed;
      flake = {
        build = nixpkgs.writeScriptBin "build" ''
            uv build
          '';
        githubActions = nix-github-actions.lib.mkGithubMatrix { checks = self.packages; };
      };
      perSystem = {
        config,
        self',
        inputs',
        pkgs,
        system,
        ...
      }: {
        formatter = pkgs.alejandra;
        devenv.shells.default = {
          imports = [./devenv.nix];
        };
      };
    };
}
