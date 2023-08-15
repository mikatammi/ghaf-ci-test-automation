{
  description = "A flake for for running Robot Framework tests";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }: let
    systems = with flake-utils.lib.system; [
      x86_64-linux
      aarch64-linux
    ];
  in
    flake-utils.lib.eachSystem systems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      packages.robot-tests = pkgs.callPackage ./Robot-Framework {
        pythonPackages = pkgs.python3Packages;
      };
      packages.default = self.packages.${system}.robot-tests;

      # Development shell
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python3.withPackages (ps:
            with ps; [
              robotframework
              robotframework-sshlibrary
            ]))
        ];
      };

      # Allows formatting files with `nix fmt`
      formatter = pkgs.alejandra;
    })
    // {
    };
}
