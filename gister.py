#!/usr/bin/python2
#/* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#* File Name : gister.py
#
#* Purpose :
#
#* Creation Date : 16-02-2012
#
#* Last Modified : Sat 25 Feb 2012 09:54:15 PM EET
#
#* Created By : Greg Liras <gregliras@gmail.com>
#
#_._._._._._._._._._._._._._._._._._._._._.*/

import mechanize
import cookielib
import sys
from config import username,password





def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print "Usage: %s filename"%sys.argv[0]
        exit(1)
    broken = filename.split(".")
    if ( len( broken ) == 1 ):
        ext = ""
    else:
        ext = broken[-1]
    URL="https://gist.github.com/login"

    f = open(filename,"r")
    text = f.read()
    f.close()

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)
    br.open(URL)

    br.select_form( nr = 1 ) 
    br["login"] = username
    br["password"] = password
    br.submit()
    
    br.select_form( nr = 1 ) 
    print "Tell me the description"
    desc = raw_input()

    br.form["description"] = desc
    br.form["file_name[gistfile1]"] = filename

    extensions = []
    for control in br.form.controls:
        if control.name == "file_ext[gistfile1]":
            for item in control.items:
                extensions.append(item.attrs['value'])

    if ext in extensions:
        br.form["file_ext[gistfile1]"] = ["."+ext]
    else:
        br.form["file_ext[gistfile1]"] = [".txt"]

    br.form["file_contents[gistfile1]"] = text

    br.submit()

    print str(br).split()[-1][:-1]

if __name__=="__main__":
    main()

