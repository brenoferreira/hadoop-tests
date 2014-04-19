#!/usr/bin/env python

import sys
import boto
from boto.s3.key import Key
from StringIO import StringIO
from gzip import GzipFile

def main(argv):

  #TODO: add your AWS IAM keys here.  S3 permissions needed.
  AWS_ACCESS_KEY_ID = 'xxx'
  AWS_SECRET_ACCESS_KEY = 'xxx'
  conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
  bucket = conn.get_bucket("aws-publicdatasets")

  for line in sys.stdin:
    l = line.strip()

    try:
      key = bucket.get_key(l)
      name = key.name.split('/')[-1]

      #Key/Values are by default, split with \t
      print "size\t%s" % str(key.size)
    except:
      e = sys.exc_info()[0]
      print "error\t%s" % str(e)

if __name__ == "__main__":
    main(sys.argv)
