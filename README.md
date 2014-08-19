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

It is based on flask python micro-framework ( http://flask.pocoo.org/ ) and python proxmox API ( https://github.com/swayf/proxmoxer )

1). pip install -r requirements.txt
2) python3 index.py
3) open http://localhost:5000/ and fille the form

WARNING: at the moment it is not yet working