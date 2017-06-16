from setuptools import setup, find_packages

setup(
  name='keyword_xtract',
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  version='0.1.1',
  description='Keyword extraction with RAKE, and keyword ranking using vector representations - created as part'
              'of a toy challenge',
  author='Belal Chaudhary',
  author_email="belalc80@gmail.com",
  url='https://github.com/BelalC/keyword_i2x',
  keywords=['keyword', 'key phrase', 'RAKE', 'word2vec'],
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      "Natural Language :: English",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3.5"]
)
