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
   
   wen no db file has been created: 
      1. flask db init
      2. flask db migrate -m "users table"
      3. flask db upgrade




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
