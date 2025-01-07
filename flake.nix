{
  description = "Finance data scraper";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      nativeBuildInputs = with pkgs; [
        (python310.withPackages (p: with p; [
          tabula-py
          setuptools
          requests
        ]))
      ];
    };
  };
}
