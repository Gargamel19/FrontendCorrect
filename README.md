[![Coverage Status](https://coveralls.io/repos/github/Gargamel19/FrontendCorrect/badge.png?branch=main)](https://coveralls.io/github/Gargamel19/FrontendCorrect?branch=main)

# Install:
## Local:
1. install Python

   1. install Virtual-Env
   2. python -m venv venv (create new venv) - in projects root dict
   3. start venv:
       1. Windows: venv\Scripts\activate
       2. Linux: source venv\Scripts\activate
   4. pip install -r requirements.txt
   5. python correct_frontend.py
   
   OR (WINDOWS)
   1. startvenv.bat
   
   when no db file has been created: 
   1. flask create_tables
   
   Add user to DB
   1. flask add_user <user_name> <user_email> <user_pw> <user_superuser_True_or_False>
       1. E.g., flask add_user matt matt@matt_mail.com matt_hard_password True




## Heroku:
connect Github with Heroku. choose the right project. 
The Reposetory contains the "Procfile" witch contains the starting parameter for Heroku

#Run
## Local:
1. start venv:
    1. Windows: venv\Scripts\activate
    2. Linux: source venv\Scripts\activate
2. python correct_frontend.py

OR (WINDOWS)
1. startvenv.bat

## Heroku:
automated

#importent:
!!! when you run this app you should take care, where youre Backend is.!!! \
you can set the backend in the .config file in the roote of the Project \
\
if you are running the Frontend and the Backend on the same System make shure to modify the Ports in the .config files in the section "[STARTVALUE]"
 
