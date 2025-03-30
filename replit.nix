{pkgs}: {
  deps = [
    pkgs.xorg.libSM
    pkgs.xorg.libICE
    pkgs.xorg.libXrender
    pkgs.xorg.libXext
    pkgs.gnumake
    pkgs.binutils
    pkgs.xorg.libX11
    pkgs.openblas
    pkgs.gcc
    pkgs.pkg-config
    pkgs.cmake
    pkgs.libGLU
    pkgs.libGL
    pkgs.postgresql
    pkgs.openssl
  ];
}
