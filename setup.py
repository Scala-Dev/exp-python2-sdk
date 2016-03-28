
from setuptools import setup

setup(
  name='exp_sdk',
  pacakges= ['exp_sdk'],
  version='1.0.0b1',
  description='EXP Python SDK',
  author='Scala',
  author_email='james.dalessio@scala.com',
  url='https://github.com/scalainc/exp-python2-sdk',
  download_url='https://github.com/scalainc/exp-python2-sdk/tarball/v1.0.0-beta1',
  install_requires=["requests", "socketIO_client"],
  license='MIT',
  keywords=['scala', 'exp', 'sdk', 'signage'],
  classifiers=[
    'Programming Language :: Python :: 2'
  ]
)
