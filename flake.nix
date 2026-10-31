{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;

      trilium-py = python.pkgs.buildPythonPackage rec {
        pname = "trilium-py";
        version = "1.4.0";
        format = "wheel";

        src = pkgs.fetchurl {
          url = "https://files.pythonhosted.org/packages/e4/b1/d15b4a39cec1ca8bedf51116c2865e70f2ab2aac5efdba29d20fdd3e98f3/trilium_py-1.4.0-py3-none-any.whl";
          # sha256 of that exact wheel, hex form (Nix accepts hex for `hash`):
          hash = "sha256:6fd8278231b1938fda2e68cdf1e2076170abf96505ef76ef5f9ad6e8da612be3";
        };

        dependencies = with python.pkgs; [
          beautifulsoup4 requests markdown2 natsort loguru pillow python-dateutil tqdm
        ];

        doCheck = false;  # upstream tests want requests-mock + a live Trilium
      };

      pythonEnv = python.withPackages (ps: [ trilium-py ]);
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.hugo pkgs.vale pkgs.ghp-import pkgs.pagefind pythonEnv ];

        shellHook = ''
          # make sure the env's `python` wins over any other interpreter on PATH
          export PATH="${pythonEnv}/bin:$PATH"

          hugo version
          vale --version

          python -c 'import trilium_py, sys; print("trilium_py OK")'
        '';
      };
    };
}
