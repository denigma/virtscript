virtscript
==========

Just a script to ease some virtualization work

Specification
-------------
What we have to do:

1). Authorize user
2). Display a form with ports
3). Write files based on the form  ( to /etc/firewall/user.hostname.dmz.inc   )
4). Display already avliable files

Getting started
--------------------

It is based on flask python micro-framework ( http://flask.pocoo.org/ ) and python proxmoxia API ( https://github.com/swayf/proxmoxer )

1). pip install -r requirements.txt
2) python index.py //yes, unfortuantely to one stupid dependency I cannot use python3
3) open http://localhost:5000/
4) put valid login
5) fill the form

WARNING: at the moment it is not yet working