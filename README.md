# VRPC - Python example
[![Build Status](https://travis-ci.org/bheisen/vrpc-python-example.svg?branch=master)](https://travis-ci.org/bheisen/vrpc-python-example)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/bheisen/vrpc-python-example/master/LICENSE)
[![GitHub Releases](https://img.shields.io/github/tag/bheisen/vrpc-python-example.svg)](https://github.com/bheisen/vrpc-python-example/tag)

This project shows how you can easily bind some C++ code and use it from within
Python.

## How to run this example

Start with cloning or downloading this project from github.

### 1. Using docker

Using docker the installation is really simple and needs - besides docker -
no dependencies on your system.

1. Build a docker image using the provided `Dockerfile`, e.g.:

    ```
    docker build . -t vrpc-python-example
    ```

2. The run the example by typing:

    ```
    docker run vrpc-python-example
    ```

### 2. On your operating system

For a local installation, make sure you have Python 3 and a C++14 capable
compiler installed.

1. Install, using:
    ```
    pip install .
    ```

2. Run
    ```
    vrpc-python-example
    ```

## How does this work?

The basic idea is that the C++ code in this project (`cpp/Bar.hpp` and
`cpp/Bar.cpp`) is compiled together with the `cpp/binding.cpp` file (which
expresses what to bind) and some sources from
[vrpc](https://github.com/bheisen/vrpc) into a regular native extension.

Technically, this extension works like a factory, able to instantiate all
registered classes and call corresponding functions on them. To use it in
Python, you need to construct an instance of `VrpcLocal`, giving it the
extension as argument:

```python
from vrpc import VrpcLocal
import vrpc_example_ext  # <-- this is the compiled C++ extension

vrpc = VrpcLocal(vrpc_example_ext)

# Now vrpc is much like a factory instance capable to create C++ instance
# and provide you with a proxy for interacting

proxy_of_cpp_instance = vrpc.create('Bar')
```

For all other details, please refer to the [documentation of
vrpc](https://github.com/bheisen/vrpc#readme)

## Writing a proper setup.py

For the binding to work it is important to have a proper setup.py:

```python
from distutils.sysconfig import get_python_lib
from setuptools import setup, Extension, find_packages
import os


vrpc_path = os.path.join(get_python_lib(), 'vrpc')
vrpc_module_cpp = os.path.join(vrpc_path, 'module.cpp')

module = Extension(
    'vrpc_example_ext',
    include_dirs=[vrpc_path, './cpp'],
    define_macros=[
        ('VRPC_COMPILE_AS_ADDON', '<binding.cpp>'),
        ('VRPC_MODULE_NAME', '"vrpc_example_ext"'),
        ('VRPC_MODULE_FUNC', 'PyInit_vrpc_example_ext')
    ],
    extra_compile_args=['-std=c++14', '-fPIC'],
    sources=[
        vrpc_module_cpp,
        './cpp/Bar.cpp'
    ],
    language='c++'
)

setup(
    name='vrpc_example',
    # [...]  Your project details
    ext_modules=[module]
)
```

It is important that the path to `vrpc` (which must be installed as a
dependency) is found.

The installation location of dependencies (and hence also `vrpc`) may vary
largely depending on your Python setup and the way you installed.

The above file will work on a "standard" Python installation, using it may fail
for non-standard installations in which you should tweak the value of the
`vrpc_path` variable manually.
