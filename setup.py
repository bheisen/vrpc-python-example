from distutils.sysconfig import get_python_lib
from setuptools import setup, Extension, find_packages
from os import path

README_md = path.join(path.abspath(path.dirname(__file__)), 'README.md')

with open(README_md, 'r') as f:
    long_description = f.read()

vrpc_path = path.join(get_python_lib(), 'vrpc')
vrpc_module_cpp = path.join(vrpc_path, 'module.cpp')

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
    name='vrpc-python-example',
    version='1.0.0',
    license='MIT',
    description='Example project demonstrating the usage of vrpc',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Burkhard C. Heisen',
    author_email='burkhard.heisen@xsmail.com',
    packages=find_packages(),
    install_requires=[
        'vrpc'
    ],
    entry_points={
        'console_scripts': [
            'vrpc-python-example = vrpc_python_example.main:main'
        ]
    },
    ext_modules=[module]
)
