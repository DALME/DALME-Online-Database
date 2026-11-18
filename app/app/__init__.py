"""Interface for the app module."""

from __future__ import annotations

import pymysql

# The ResourceSpace DAM is MySQL. PyMySQL stands in for mysqlclient behind the
# `MySQLdb` interface, which Django's mysql backend and the DAM's legacy manager
# both import, so nothing native has to be built on the host or in the images.
pymysql.install_as_MySQLdb()
