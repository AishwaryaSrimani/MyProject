from flask import Flask, redirect, url_for, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

db_config = {
        'user':'root', 
        'password':'yashjha123',
        'host':'localhost',
        'database':'users'
    }

def write_to_mysql(ussername, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS info (
            Username VARCHAR(255) NOT NULL,
            Password VARCHAR(255) NOT NULL,
            CONSTRAINT UC_Info UNIQUE (Username, Password)
        )
    ''')
    connection.commit()
    
    query = 'insert into info (username, password) values (%s, %s)'
    cursor.execute(query, (ussername, password))
    connection.commit()
    
    if connection.is_connected():
        cursor.close()
        connection.close()
        
                
def check_login_credentials(username, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    query = 'select * from info where username = %s and password = %s'
    cursor.execute(query, (username, password))
        
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return result is not None  


def update_pass(username, password, new_password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = 'update info set password = %s where username = %s and password = %s'
    
    cursor.execute(query, (new_password, username, password))
    
    connection.commit()
    
    connection.close()
    cursor.close()

def delete_account(username, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = 'delete from info where username = %s and password = %s'
    cursor.execute(query, (username, password))
    
    connection.commit()
    
    connection.close()
    cursor.close()
    return True


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        write_to_mysql(username, password)
        
        return redirect(url_for('login'))
    else:
        return render_template('register.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check_login_credentials(username, password)
        
        return 'success'
        
    return render_template('login.html')


# @app.route('/update', methods=['GET', 'POST'])
# def update():
#     if request.method == 'POST':
#         username = request.form['username']  # Assuming the form contains a field for the username
#         password = request.form['password']
#         new_password = request.form['new_password']
#         if update_pass(username, new_password):
#             return 'success'
#         else:
#             return 'failed'
#     return render_template('update.html')

@app.route('/change_password', methods=['PUT', 'GET'])
def change_pass():
    try:
        if request.method == 'PUT':
            username = request.json.get('username')
            password = request.json.get('password')
            new_password = request.json.get('new_password')
            
            if check_login_credentials(username, password) == True:
                update_pass(username, password, new_password)
                return 'success'
            else:
                return 'failed'
    except Exception as e:
        return (f'an error occur: {str(e)}')

    return render_template('update.html')

@app.route('/delete_acc', methods=['DELETE', 'GET'])
def delete_acc():
    if request.method == 'DELETE':
        username = request.json.get('username')
        password = request.json.get('password')

        if check_login_credentials(username, password) == True:
            delete_account(username, password)
            return redirect(url_for('register'))
        else:
            return 'failed'

    return render_template('delete.html')
    
        
        

if __name__ == "__main__":
    app.run(debug=True, port=8000)