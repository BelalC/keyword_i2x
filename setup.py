from distutils.core import setup

setup(
  name='keyword_xtract',
  packages=['keyword_xtract'], # this must be the same as the name above
  version='0.1',
  description='Keyword extraction with RAKE, and keyword ranking using vector representations - created as part'
              'of a toy challenge',
  author = 'Belal Chaudhary',
  url = 'https://github.com/BelalC/keyword_i2x', # use the URL to the github repo
  download_url = 'https://github.com/peterldowns/mypackage/archive/0.1.tar.gz',
  keywords = ['keyword', 'key phrase','RAKE', 'word2vec'], # arbitrary keywords
  classifiers = [],
)