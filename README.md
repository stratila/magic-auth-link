### About
The application allows a user to login by the "magic" link that is sent to the entered email. After authorization a user is stayed logged in in the application where they are able to see how many times they tap the active link (the link has expiration time). A user can log out of the application or application will log out automatically after a minute of inaction. I chose to do the appliaction with Flask because it has convinient extentions such as Flask-Login, Flask-Mail, Flask-SQLAlchemy, etc. These extentions allows us to prorotyping the applications in the fast way. Further, for "magic" link generation I chose JSON Web Token library, wich allowed us to decode some data in JSON format and set the expiration time.