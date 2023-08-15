{
  lib,
  buildPythonPackage,
  fetchPypi,
}:
buildPythonPackage rec {
  version = "0.3.0";
  pname = "install-requires";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-1iKUhuCFozAEHTzG9H7rjS/QwlXPgaS4mbKHwwbetxc=";
  };

  # unit tests are impure
  doCheck = false;

  meta = with lib; {
    description = "";
    homepage = "https://github.com/orsinium-archive/install-requires";
    license = licenses.asl20;
  };
}
