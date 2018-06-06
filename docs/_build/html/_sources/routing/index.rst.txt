Routing
=======

This is the broad heading to group together the files that determine how a
given URL translates into an actual page. There are two main components to
this process, the `urls.py` file and the `views.py` file. Generally, `urls.py`
determines which function will run in response to a request for a url,
referring to some function by name, while views.py handles the actual
execution of those functions, which render various HTML templates.

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  urls
  views
