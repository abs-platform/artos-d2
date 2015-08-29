#!/usr/bin/python
# Translation from a bug report to a HTML page.
# Both the bug report and the HTML page are custom-made. They follow no 
# formal standard.
#
# Authors:
#  Marc Mari <marc.mari.barcelo@gmail.com>
#
# This work is licensed under the terms of the GNU GPL, version 2.
# See the COPYING file in the top-level directory.

import sys
import os
import shutil

html_pre_title = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <title>'''

html_post_title = '''
</title>
    <link rel="stylesheet" href="../stylesheets/styles.css">
    <link rel="stylesheet" href="../stylesheets/github-dark.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    <script src="../javascripts/respond.js"></script>
    <!--[if lt IE 9]>
      <script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <!--[if lt IE 8]>
    <link rel="stylesheet" href="../stylesheets/ie.css">
    <![endif]-->
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">

  </head>
  <body>
      <div id="header">
        <nav>
          <li class="fork"><a href="https://github.com/mark-mb/artos-d2">View On GitHub</a></li>
          <li class="downloads"><a href="https://github.com/mark-mb/artos-d2/zipball/master">ZIP</a></li>
          <li class="downloads"><a href="https://github.com/mark-mb/artos-d2/tarball/master">TAR</a></li>
          <li class="title">DOWNLOADS</li>
        </nav>
      </div><!-- end header -->

    <div class="wrapper">

      <section>
        <div id="title">
          <h1>ARTOS-D2</h1>
          <p>Android Real Time Operating System</p>
          <hr>
          <span class="credits left">Project maintained by <a href="https://github.com/mark-mb">mark-mb</a></span>
          <span class="credits right">Hosted on GitHub Pages &mdash; Theme by <a href="https://twitter.com/michigangraham">mattgraham</a></span>
        </div>'''

html_footer = '''
      </section>

    </div>
    <!--[if !IE]><script>fixScale(document);</script><![endif]-->
    
  </body>
</html>
'''

# First argument: bug import folder
# Second argument: html and bug export folder
if len(sys.argv) != 3:
    print("Exactly two arguments are expected: 1) Source folder 2) Destination folder")
    sys.exit(1)

input_dir = sys.argv[1]
if not os.path.isdir(input_dir):
    print("Folder " + input_dir + " does not exist")
    sys.exit(1)

output_dir = sys.argv[2]
if not os.path.isdir(output_dir):
    print("Folder " + output_dir + " does not exist")
    sys.exit(1)

bugs = []
for filename in os.listdir(input_dir):
    if filename == '.' or filename == '..':
        continue

    bug_number, _ = os.path.splitext(os.path.basename(filename))
    if int(bug_number) == 0:
        print("File " + filename + " doesn't have a valid name.")
        continue

    input_file = input_dir + "/" + filename
    output_file = output_dir + "/bug" + bug_number
    with open(input_file, "r") as bugfile:
        with open(output_file + ".html", "w") as outfile:
            bugs.append(bug_number)

            outfile.write(html_pre_title)
            outfile.write("Bug " + bug_number)
            outfile.write(html_post_title)

            first_line = True
            pre = False
            for line in bugfile:
                # This won't appear in a Linux trace, hopefully
                if line.find("----------") != -1:
                    line = line.replace('\n', '')
                    line = line.replace('-', '')

                    if first_line:
                        first_line = False
                    else:
                        if pre:
                            outfile.write("</pre>\n")
                            pre = False
                        else:
                            outfile.write("</p>\n")

                    outfile.write("<h2>" + line + "</h2>\n")

                    if line.find("Log") != -1:
                        outfile.write("<pre>")
                        pre = True
                    else:
                        outfile.write("<p>")

                else:
                    outfile.write(line)

            outfile.write(html_footer)

        shutil.copyfile(input_file, output_file + ".txt")

with open(output_dir + "/bugs.html", "w") as outfile:
    outfile.write(html_pre_title)
    outfile.write("Bugs found while debugging ARTOS")
    outfile.write(html_post_title)

    bugs.sort()

    for bug in bugs:
        outfile.write("Bug " + bug + " [ ")
        outfile.write('<a href="bug' + bug + '.txt">Plain</a>')
        outfile.write(" | ")
        outfile.write('<a href="bug' + bug + '.html">HTML</a>')
        outfile.write(" ] <br/>\n")

    outfile.write(html_footer)
