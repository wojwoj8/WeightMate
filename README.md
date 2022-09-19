# WeightMate
#### Video Demo:  <https://youtu.be/7Pxf-4vhfDI>
#### Description: Bodyweight tracker/Diet assistance
## **What is WeightMate?**
WeightMate is my first project ever. It is a full stack web application created with Flask, SQL, HTML, CSS and a little bit of JavaScript. Its main goal is to help people achieve or maintain their dream weight by following a calculated diet.
## **Layout**
Nearly every page extendes the layout.html template where are :title block, main block and somewhere messages. It is handled with Jinja2 and Flask. Other things are: navbar from bootstrap, css files and html, body, main tags.
## **Start page (notlogged)**
Start page consists of CSS animation showing web name and Sign up button. Navbar contains retirection to notlogged page,  sign up and log in links.
## **Sign up**
Sign up page has three fields: first for username, second for password and the last one for password confirmation. Here validation is created with JavaScript, if user input already existing username or passwords doesn't match or fields are empty, proper error message will appear. If user is not logged, other pages than that in navbar will redirect to notlogged page. After successfully Sing up we are redirected to getstarted form.
## **Getstarted**
Here we have to fill out the form where we give our age, height, weight, gender, activity level, terget weight and rate of weight change. There is validation both in frontend and backend, and when form doesn't match given criteria, than proper error message will appear. If user don't fill the form, only logout link will work and clear session data. This prevention is created because there are crucial data from which calories will be calculated. After successfully filled out form user is redirected to main page.
## **Log in**
Login page is basically Sign up page without password confirmation, validation is the same, at backend it looks in users.db for given username and password, which is hashed. When user login than appears main page.
## **Main page (index)**
There user can see already calculated calories which need to be consumed every day to achive their goal. It also show the date when the goal will be achived. Also there is a line chart created with chart.js that show user weight in time. Below is an add button which redirect to form where user can add some body circuits, weight and day of measurement to the database. Navbar links are changed to profile and measurements. In measurements user can see a table in which is every measurement sorted by date.
## **Profile**
In profile are three buttons, clicking on the first one will redirect to modprof page where we can change our username, passwor, age, height and gender. Of course there is a proper validation like before. To modify user have to press modify button below form. Second one will redirect user to the measurements table, and the last one will redirect to form where users can change their goal weight, rate and activity level. After any change, calories will be calculated again and it can affect the goal date.
## **Files.py**
The app.py is a backend side of the webapp. app.py uses Flask, SQL, werkzeug.security for hashing passwords, addfunc.py for wrapping functions with loggin @login_required function which blocks some pages until user logs in, and @startform_required form which blocks some pages until user fill the getstarted form. Almost whole app.py is just getting data from user, validating that, reading from or writing to database, and some calculations.
## **Users.db**
Users database consists of two tables. The first one is users table where primary key is autoincrement not null id, next are text not null username and hash(hashed password), than height, age, gender, activity, tdee which is Total Daily Energy Expenditure (calories), bmr - Basal metabolic rate, and goal.
Second one is measurements table which contains user_id as foreign key referencing to users(id), and all numeric measurements like arm, nech, biceps, etc.


