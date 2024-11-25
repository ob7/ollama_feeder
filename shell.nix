# ollama_feeder/shell.nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.sentence-transformers
    pkgs.python3Packages.faiss
    pkgs.git
  ];
}

