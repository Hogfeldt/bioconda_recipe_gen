str_to_pkg = {
    "autoheader: not found": ("autoconf", "build"),
    "autoreconf: command not found": ("automake", "build"),
    "autoreconf: failed to run aclocal": ("automake", "build"),
    "could not find hdf5": ("hdf5", "host"),
    "unable to find the requested boost libraries": ("boost", "host"),
    "could not find boost": ("boost", "host"),
    "no cmake_cxx_compiler could be found": ("{{ compiler('cxx') }}", "build"),
    'could not find a package configuration file provided by "seqan"': ("seqan-library", "build"),
    "could not find bison": ("bison", "build"),
    "bison: command not found": ("bison", "build"),
    "could not find flex": ("flex", "build"),
    "flex: command not found": ("flex", "build"),
    "could not find libxml2": ("libxml2", "build"),
    "could not find armadillo": ("armadillo", "host"),
    "error: libtool library used but": ("libtool", "build"),
    "could not find blas (missing: blas_libraries)": ("openblas", "host")
}