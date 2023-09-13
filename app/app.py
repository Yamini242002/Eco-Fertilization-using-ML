from flask import Flask, render_template, request, url_for
from BestTimeToFertilizeModule import BestTimeToFertilize
from NPKEstimatorModule import NPKEstimator
from flask import Flask, render_template, request, session, url_for, redirect, jsonify,make_response
 
#import sqlite3

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Set up the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Create a user class
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_active = True
    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create a dummy user
user = User(id=1, username='user', password='password')

# Store users in a dictionary (in a real application, you would store them in a database)
users = {user.username: user}
app.secret_key = 'secret-ley'
# Set up the login view
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['passw']
        if username=="admin" and password=="admin":
            return render_template('index.html')    
        if username in users and users[username].check_password(password):
            login_user(users[username])
            return render_template('index.html')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# Set up the registration view
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['passw']
        if username=='' or password=='':
            return render_template('register.html')
        if username in users:
            return 'Username already exists'
        else:
            new_user = User(id=len(users) + 1, username=username, password=password)
            users[username] = new_user
            login_user(new_user)
            return render_template('index.html')
    return render_template('register.html')

 
# Set up the logout view
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are logged out'

# Set up the login manager
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None


@app.route("/")
def index():
    return render_template("home.html")




 

@app.route('/processing/', methods=['GET', 'POST'])
def processing():
    # print('Processing......')
    if request.method == "GET":
        print("The URL /processing is accessed directly.")
        return url_for('index.html')

    if request.method == "POST":
        form_data = request.form
        call_success = []
        npk_list_dict = []
        popup_data = []
        seven_days = []

        crop = form_data['crop']
        state = form_data['state']
        city = form_data['city']

        with open("InputData.csv", "w") as fh:
            input_data = "%s,%s,%s" % (crop.strip(), state.strip(), city.strip())
            fh.write(input_data)
        
        bttf = BestTimeToFertilize(city_name = city, state_name = state)
        bttf.api_caller()

        if bttf.is_api_call_success():
            category, heading, desc = bttf.best_time_fertilize()

            call_success.append(1)
            popup_data.append([category, heading, desc])
            seven_days = bttf.weather_data[:]
            # print(seven_days)
            
            # today's weather data
            di = bttf.weather_data[0]
            temp = di['Temperature']
            humidity = di['Relative Humidity']
            rainfall = di["Rainfall"]

            est = NPKEstimator()
            est.renameCol()

            npk = {'Label_N':0, 'Label_P':0, 'Label_K':0}
            for y_label in ['Label_N', 'Label_P', 'Label_K']:
                npk[y_label] = est.estimator(crop, temp, humidity, rainfall, y_label)
            # print(npk)

            npk_list_dict.append(npk)

            output_data = category +"\n"+ heading +"\n"+ desc +"\n"+ str(npk['Label_N'])  +"\n"+ str(npk['Label_P'])  +"\n"+ str(npk['Label_K'])
            with open("output.txt", "w") as fh:
                fh.write(output_data)
        else:
            print("Error Occured")
        #print(call_success, npk_list_dict, form_data, popup_data)
        return render_template('update.html', CALL_SUCCESS = call_success, NPK = npk_list_dict, FORM_DATA = form_data, POPUP_DATA = popup_data, SEVEN_DAYS = seven_days)
    

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     return render_template('index.html')


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)