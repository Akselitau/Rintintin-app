Rintintin is a reservation system project for dog daycare and boarding services. 


Start the Local Database
Make sure your local PostgreSQL database is configured and running.
setup your .env with the variables of your database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=doggydb
DB_USER=mydbuser
DB_PASSWORD=mypassword

BACKEND
- Create a new virtual environment and install the dependencies:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

- Start the backend using Chalice:
cd API
chalice local

- The backend will be accessible at:
http://127.0.0.1:8000

- Call create-tables.py
- Call populate-database.py


FRONTEND
- Install the dependencies and start the frontend:
cd dog-reservation-frontend/
npm install
npm start
The frontend will be accessible at:
http://localhost:3000


How to Use the Project

The project is still in its early stages, and some features may not be fully functional yet. I apologize for any "not working yet" features.

Code Information

Comments: There are a lot of comments in the frontend code because I am currently learning new things about it.
Code Review: My code has not been reviewed by anyone yet, so I apologize in advance for any mistakes or inconsistencies you might encounter.
