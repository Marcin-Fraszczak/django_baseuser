## Simple web app required for testing

To run it locally:

1) Clone the repo:

``git clone git@github.com:Marcin-Fraszczak/django_baseuser.git``

2) Inside the root directory (Docker needed, ~20 seconds):

`docker-compose up``

3) This will create and run the container with Django app, autmotically create the database and should open the browser.If not you can manually navigate to :

``localhost:8000``

4) While using the app, you can choose 'Tests' from navbar and run automatic tests from inside the app.
5) Report will be created and displayed in html.
6) On the report you can click 'Show all details' to reveal documentation for testing.

------------------

7) If you want to send real emails, create ``.env`` file in the root directory and populate it with data based on ``.env_sample`` file.
8) Not doing this is still ok, django has it's own simple smtp server, to enable it and see emails in the console, do the following:
    * open another terminal and type: ``docker ps``
    * on returned list of containers find a name of running container and enter its shell: ``docker exec -it <container_name> sh``
    * in the shell type: ``python -m smtpd -n -c DebuggingServer localhost:1025``
