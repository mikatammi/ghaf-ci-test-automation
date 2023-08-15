{
  lib,
  buildPythonPackage,
  fetchPypi,
  robotframework,
  pyserial,
  install-requires,
}:
buildPythonPackage rec {
  version = "0.4.3";
  pname = "robotframework-seriallibrary";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-8gvv5cEQbdjdyp9govGL9ex9Xwb28JoD+ma65Ud35rs";
  };

  # unit tests are impure
  # doCheck = false;

  nativeBuildInputs = [install-requires];

  propagatedBuildInputs = [robotframework pyserial];

  meta = with lib; {
    description = "Robot Framework test library for serial connection";
    homepage = "https://github.com/whosaysni/robotframework-seriallibrary/blob/develop";
    license = licenses.asl20;
  };
}
