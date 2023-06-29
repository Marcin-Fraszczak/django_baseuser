## Simple web app required for testing

To run it locally:

1) Clone the repo:

``git clone git@github.com:Marcin-Fraszczak/django_baseuser.git``

2) Inside the root directory (Docker needed):

``docker-compose up``

3) This will create and run the container with Django app, autmotically create the database and should open the browser.If not you can manually navigate to :

``localhost:8000``

4) While using the app, you can choose 'Tests' from navbar and run automatic tests from inside the app.
5) Report will be created and displayed in html.
6) On the report you can click 'Show all details' to reveal documentation for testing.