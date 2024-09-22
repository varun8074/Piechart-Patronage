from flask import Flask, render_template, request
import mysql.connector


app = Flask(__name__)



# MySQL configuration
mysql_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'project'
    }
  # Create a connection to the database
db = mysql.connector.connect(**mysql_config)

# Create a cursor object to execute SQL queries
cursor = db.cursor()





@app.route("/")
def home():
    return render_template("home.html")


@app.route("/registration_form", methods=["GET", "POST"])
def registration_form():
        return render_template("registration_form.html")

# Save the form data to the database
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get the form data
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    color = request.form['color']
    favourite_place = request.form['favourite_place']


   # Check if email already exists in the database
    email_exists_sql = "SELECT COUNT(*) FROM users WHERE email = %s"
    cursor.execute(email_exists_sql, (email,))
    email_exists = cursor.fetchone()[0]

    # Check if name already exists in the database
    email_exists_sql1 = "SELECT COUNT(*) FROM users WHERE name = %s"
    cursor.execute(email_exists_sql1, (name,))
    email_exists1 = cursor.fetchone()[0]



    
    if email_exists > 0 or email_exists1>0:
        # Email already exists, show an error message or redirect to a failure page
        return render_template('email_exists.html')
    
    # Insert the form data into the database
    sql = "INSERT INTO users (name, email, password, color,favourite_place) VALUES (%s, %s, %s, %s,%s)"
    values = (name, email, password, color, favourite_place)
    cursor.execute(sql, values)
    db.commit()
    
    # Redirect the user to a success page
    return render_template('success.html')



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="project"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE name = %s"
        value = (name,)

        cursor.execute(query, value)
        result = cursor.fetchone()

        if result:
            
            query1="select color from users where name=%s"
            value1=(name,)
 
            cursor.execute(query1, value1)
            result1 = cursor.fetchone()           

            return render_template('authenticate_user.html', user_color=result1[0])
            

        else:
            return "Login failed."

    return render_template("login.html")



@app.route("/authenticate_user", methods=["GET", "POST"])
def authenticate_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="project"
        )

        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        user = cursor.fetchone()

        if user:
            return "login successful...."
        else:
            return render_template("wrong_password.html")

    return render_template("cir1.html") 



@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

        return render_template("forgot_password.html")


@app.route("/forgot_password_authentication", methods=["GET", "POST"])
def forgot_password_authentication():
        if request.method == "POST":
            email = request.form["email"]
            favourite_place = request.form["favourite_place"]
            newPassword = request.form["newPassword"]

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="pj"
        )

            cursor = conn.cursor()


            # Update the password
            update_query = "UPDATE users SET password = %s WHERE email = %s AND favourite_place = %s"
            values = (newPassword, email, favourite_place)

            #cursor = connection.cursor()
            cursor.execute(update_query, values)
            conn.commit()
                
            if cursor.rowcount > 0:
                return"Password updated successfully"
            else:
                return "No records updated"


if __name__ == "__main__":
    app.run(debug=True)
