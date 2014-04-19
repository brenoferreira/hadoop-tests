#!/usr/bin/env python

import sys

def main():
    #TODO: Update this to only print one line, the total summed value of all 'size' keys

    for line in sys.stdin:
      line = line.strip()

      try:
        key,val = line.split('\t',1)
        print key + "\t" + val

      except:
        #e = sys.exc_info()[0]
        print "error\ttest"

def test():
  sys.stdin = ['size\t634445874\n','size\t634445874','size\t634445874', 'test\n', 'best']

if __name__ == "__main__":
  #test()
  main()


