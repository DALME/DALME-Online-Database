# Tenant File Overrides

To selectively override templates and static files on a per tenant basis you
can add files to these directories and the Django static files resolver will
prefer whatever it finds here at `collectstatic` time.

Needless to say you have to follow the correct directory structure and file
naming conventions in order to achieve this. If you have any doubts you can
consult either the template directories in the source tree or the
`app/www/static` directory which is created when you call `make
app.collectstatic`.

Inside that directory you can see how `collectstatic` creates a separate static
files distribution for each registered tenant. If you create a file override
(and put it in the right place in the overrides directory tree) then the
`collectstatic` command will just copy over the override file in place of the
original file. It doesn't do anything cleverer than that.
