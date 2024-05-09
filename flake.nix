{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs: inputs.flake-utils.lib.eachDefaultSystem (system: let
    pkgs = import inputs.nixpkgs { inherit system; };

    python_version = pkgs.python310;
    pythonpkg = python_version.withPackages (p: with p; [
      pydbus
      pygobject3
      gst-python
      pydub
    ]);

    deps = with pkgs; [
      pythonpkg
      mpg123
    ];

  in {
    devShells.default = pkgs.mkShell {
      buildInputs = deps;
      shellHook = ''
        export PATH="$PATH:$(realpath ./)"
        source ./autocomplete.sh
      '';

      PYTHONPATH = "${pythonpkg}/${pythonpkg.sitePackages}:$PYTHONPATH";
      LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib$LD_LIBRARY_PATH";
    };
  });
}
