# PWMAN3 

A nice command line password manager, which is smart enough to use different SQL Databases (MySQL, SQLite, BerkelyDB).  
Pwman3 can also copy passwords to the clipboard (on Mac and Linux) without exposing them, so you save
some typing. 
Besides managing and storing passwords, Pwman3 can also generate passwords using different algorithms. 


== Installing ==

Pwman3 requires the following debian packages:
	
when using python 2.4    
    python-pysqlite2
	python-celementtree
    python-crypto
when using python >= 2.5 
    python-crypto


for nicer functionality:
    xsel - to copy password to clipboard on Linux

To install:

$ python setup.py install

== ikegam's function ==

 * making a password from the numeric character and the alphabet character ([A-Za-z0-9]).

   You can add a parametor for making the password to the config(~/.pwman/config).

   For Example)
     [Generator]
     numerics = true
     
 * Passwords can be l33tified similarly using the following.
     [Generator]
     leetify = true
 
 * Copying password to X11 or Mac clipbord:
  - On Mac OSX systems copying utilizes `pbcopy`  
  - On X11 Systems  Specify the path to `xsel` if you already have `~/.pwman/config` 
      [Global]
      xsel = yes
      xselpath = /usr/bin/xsel

 
     When launching `pwman` for the first time, it will try and look for 
     `xsel` and write the configuration properly. 

