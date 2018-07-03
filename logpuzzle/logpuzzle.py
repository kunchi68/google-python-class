#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  match = re.search(r'\w+_(.+)', filename)
  if not match:
      sys.stderr.write("Incorrect filename: " + filename + "\n");
      sys.exit(1)
  #print match.group(1)
  server_name = match.group(1)

  dict = {}
  urls = []
  f = open(filename, 'rU')
  for line in f:
      match = re.search(r'GET (\S+-\S+-(\S+)\.jpg) HTTP/1.0', line)
      if match : 
          pic = match.group(1)
          w2 = match.group(2) 
          #print match.group(2) 
          if not pic in urls : dict[w2] = pic
          continue

      match = re.search(r'GET (\S+\.jpg) HTTP/1.0', line)
      if match : 
          pic = match.group(1)
          if not pic in urls : urls.append(pic)
  f.close()

  urls = sorted(urls)
  keys = sorted(dict.keys())
  for key in keys: urls.append(dict[key])
  urls = [ "http://" + server_name + url for url in urls]
  return urls
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  # Create dest_dir if it does not exist.
  if not os.path.exists(dest_dir) :
      os.makedirs(dest_dir)

  # Download image to dest_dir
  num = 0
  for url in img_urls:
      dest_path = dest_dir + "/img" + str(num)
      print("Retrieving %s to %s (%d/%d)" %(url, dest_path, num+1, len(img_urls)))
      urllib.urlretrieve(url, dest_path)
      num += 1

  # Create index.html in dest_dir with image info.
  f = open(dest_dir + "/index.html", "w")
  f.write("<html><body>\n")
  for i in range(num):
      f.write('<img src="' + "img" + str(i)  + '">')
  f.write("\n")
  f.write("</body></html>\n")
  f.close()

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
