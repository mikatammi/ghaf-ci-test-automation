{
  pythonPackages,
  stdenv,
}:
stdenv.mkDerivation {
  pname = "robot-tests";
  version = "0.0.1";
  src = ./.;
  buildInputs = [
    pythonPackages.robotframework
    pythonPackages.robotframework-sshlibrary
  ];
  installPhase = ''
    mkdir -p $out
    cp -rv config lib resources test-suites $out

    # WORK IN PROGRESS
  '';
}
