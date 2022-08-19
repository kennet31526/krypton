import pathlib
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from pybind11.setup_helpers import Pybind11Extension
import os
import sys

DEBUG = sys.argv.count("--debug") >= 1

description = open("README.md", "r").read()

extra_args = []
if DEBUG and sys.platform != "win32":
  extra_args += ["-g"]
if not DEBUG and sys.platform != "win32":
  extra_args += ["-O2"]
if not DEBUG and sys.platform == "win32":
  extra_args += ["/O2"]

link_libararies = ["crypto", "ssl"]
macros = []
runtime_libs = ["kr-openssl-install/lib64", "kr-openssl-install/lib"]
if sys.platform == "win32":
  link_libararies = ["libcrypto", "user32", "WS2_32", "GDI32", "ADVAPI32", "CRYPT32"]
  macros += [("WIN", None)]
  runtime_libs = []

def finishInstall():
  openssl_fips_module = "kr-openssl-install/lib/ossl-modules/fips.dll" if sys.platform == "win32" else "kr-openssl-install/lib64/ossl-modules/fips.so" 
  openssl_fips_conf = "kr-openssl-config/fipsmodule.cnf"
  openssl = '"kr-openssl-install\\bin\\openssl"' if sys.platform == "win32" else './kr-openssl-install/bin/openssl'
  pysec_data = pathlib.Path(pathlib.Path.home(), ".krypton-data/")
  if not pysec_data.exists():
    os.mkdir(pysec_data.as_posix())
  os.system(f'{openssl} fipsinstall -out {openssl_fips_conf} -module {openssl_fips_module}')

class completeInstall(install):
  def run(self):
    temp = os.getcwd()
    install.run(self)
    try: os.chdir(os.path.join(self.install_base, "site-packages/"))
    except FileNotFoundError: 
      try: os.chdir(os.path.join(self.install_base, "Lib/site-packages/"))
      except FileNotFoundError: return
    finishInstall()
    os.chdir(temp)

class completeDevelop(develop):
  def run(self):
    temp = os.getcwd()
    develop.run(self)
    os.chdir(pathlib.Path(__file__).parent.as_posix())
    finishInstall()
    os.chdir(temp)

setup(name='krptn',
  version='1.0',
  description='A user authentication and access management system based entirely on cryptographic primitives.',
  long_description=description,
  long_description_content_type="text/markdown",
  author='Krypton Project',
  author_email='contact@krptn.dev',
  project_urls={
    'Bug Tracker': "https://github.com/krptn/krypton/issues",
    'Homepage': "https://www.krptn.dev/",
    'Documentation': "https://docs.krptn.dev/",
    'GitHub': "https://github.com/krptn/krypton/"
  },
  classifiers=[
      'License :: OSI Approved :: Apache Software License',
      'Operating System :: OS Independent',
      'Intended Audience :: Developers',
      'Intended Audience :: System Administrators',
      'Topic :: Security',
      'Topic :: Security :: Cryptography',
      'Framework :: Django',
      'Framework :: Flask'
  ],
  package_data={"":["../kr-openssl-install/bin/libcrypto-3-x64.dll",
    "../kr-openssl-install/lib/ossl-modules/fips.dll",
    "../kr-openssl-install/bin/openssl.exe",
    "../kr-openssl-config/openssl.cnf",
    "../kr-openssl-config/fipsmodule.cnf",
    "../kr-openssl-install/bin/openssl",
    "../kr-openssl-install/lib64/libcrypto.so",
    "../kr-openssl-install/lib64/libcrypto.a",
    "../kr-openssl-install/lib64/ossl-modules/fips.so",
    "../kr-openssl-install/lib64/libcrypto.so.3",
    "../kr-openssl-install/lib64/libssl.so.3",
    "../kr-openssl-install/lib64/libssl.so",
    "../kr-openssl-install/lib/libcrypto.so",
    "../kr-openssl-install/lib/libcrypto.a",
    "../kr-openssl-install/lib/ossl-modules/fips.so",
    "../kr-openssl-install/lib/libcrypto.so.3",
    "../kr-openssl-install/lib/libssl.so.3",
    "../kr-openssl-install/lib/libssl.so"]},
  packages=['krypton'],
  python_requires=">3.8",
  install_requires=["SQLAlchemy", "webauthn"],
  extras_require={
        "MSSQL": ["pyodbc"],
        "MySQL": ["mysqlclient"],
        "PostgreSQL": ["psycopg2"],
        "Django": ["django"],
        "Flask": ["flask"]
  },
  include_package_data=True,
  cmdclass={
    'install': completeInstall,
    'develop': completeDevelop
  },
  ext_modules=[Pybind11Extension('__CryptoLib',
    ["CryptoLib/CryptoLib.cpp", "CryptoLib/aes.cpp", "CryptoLib/ecc.cpp", 
      "CryptoLib/hashes.cpp", "CryptoLib/bases.cpp", "CryptoLib/OTPs.cpp"],
    include_dirs=["kr-openssl-install/include", "CryptoLib"],
    library_dirs=["kr-openssl-install/lib", "kr-openssl-install/lib64"],
    libraries=link_libararies,
    runtime_library_dirs=runtime_libs,
    extra_compile_args=extra_args,
    extra_link_args=extra_args,
    define_macros=macros)],
)
