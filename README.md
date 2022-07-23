# Booklet-Repository-django
This project is a basic booklet repository model made using Django

This booklet repository contains a login page for the existing users to login and a signup page using email or google authentication for new users to register. If registered via email id then it asks for a confirmation to click link in the email sent by the server. There after login, user can see all the booklets in pdf format uploaded by the admin and can view or download them.

If admin is logged in, then in admin page, admin can see all the uploaded booklets and has access to delete or add a new one and also can see the users who are logged in for the website.

Initially for the testing purpose I have uploaded 3 pdf files in the backend to check the functioning of the web app.

For this project, majorly I used,
1. django-all-auth, a django built in feature to authenticate accounts using social media like google, facebook etc...
2. A password reset token generator to authenticate provided emails using unique tokens.
3. A python module named "six" to get the new string object from a given string object using text_type() function
4. messages feature in django to show some success and error messages
5. Email message feature from django to send email automatically from server by using google app password feature because of non-existance of "low-security            apps" option from May 31, 2022.


The "bin" folder, "pyvenv.cfg" file are a part of virtual environment. I tried to include complete python3.10 as a part of virtualenvironment but github is not accepting it.So, in my virtual environment there is a folder named "bin" which i have uploaded, "include" which is empty, "lib" which has complete python3.10 and i had not uploaded here and a 'pyvenv.cfg"file which i have uploaded.
