{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.hugo pkgs.vale pkgs.python3 pkgs.ghp-import pkgs.pagefind ];
        shellHook = ''
          hugo version
          vale --version
        '';
      };
    };
}
