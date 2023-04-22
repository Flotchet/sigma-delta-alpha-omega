from flask import Flask, render_template, request, Markup, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from waitress import serve
import pickle
import os
import pandas as pd
import datetime
import os
import csv
import sqlite3
import pandas
import secrets
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.compose import make_column_selector as selector
import hashlib


######################################################################################app config
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates', static_folder='templates/assets')

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'databases/fin.db') 
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///' + os.path.join(basedir, 'databases/users.db'),
    'churn': 'sqlite:///' + os.path.join(basedir, 'databases/churn.db'),
    'followed': 'sqlite:///' + os.path.join(basedir, 'databases/followed.db')}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["DEBUG"] = False

db = SQLAlchemy(app)



###########################################################################real estate functions
#real estate
def RE_prepare_zipcode(df : pd.DataFrame) -> dict[int:float]:
    #create zipcode conversion table
    zipcode = {}

    #dropnan from prices
    df2 = df.dropna(subset=['Price'])
    #dropnan from zipcode
    df2 = df2.dropna(subset=['zipcode'])

    for z in list(df2['zipcode'].unique()):
        zipcode[z] = df2[df2['zipcode'] == z]['Price'].median()
        
    return zipcode

#real estate
def RE_prepare_type(df : pd.DataFrame) -> dict[str:float]:
    #create type conversion table
    types = {}

    #dropnan from prices
    df2 = df.dropna(subset=['Price'])
    #dropnan from type
    df2 = df2.dropna(subset=['type'])

    for i in df["type"].unique():
        types[i] = df[df['type'] == i]['Price'].mean()

    return types

#real estate
def RE_prepare_tax(df : pd.DataFrame) -> dict[int:float]:
    #create zipcode conversion table
    zipcode = {}

    #dropnan from tax
    df2 = df.dropna(subset=['Taxe'])
    #dropnan from zipcode
    df2 = df2.dropna(subset=['zipcode'])

    for z in list(df2['zipcode'].unique()):
        zipcode[z] = df2[df2['zipcode'] == z]['Taxe'].mean()

    return zipcode

#real estate
def RE_get_name(zipcode : int) -> str:

    if zipcode < 1300:
        return 'BruxellesCapitale'
    elif zipcode < 1500:
        return 'ProvinceduBrabantwallon'
    elif zipcode < 2000:
        return 'ProvinceduBrabantflamand'
    elif zipcode < 3000:
        return 'ProvincedAnvers'
    elif zipcode < 3500:
        return 'ProvinceduBrabantflamand2'
    elif zipcode < 4000:
        return 'ProvincedeLimbourg'
    elif zipcode < 5000:
        return 'ProvincedeLiege'
    elif zipcode < 6000:
        return 'ProvincedeNamur'
    elif zipcode < 6600:
        return 'ProvinceduHainaut1'
    elif zipcode < 7000:
        return 'ProvincedeLuxembourg'
    elif zipcode < 8000:
        return 'ProvinceduHainaut2'
    elif zipcode < 9000:
        return 'ProvincedeFlandreOccidentale'
    elif zipcode < 10000:
        return 'ProvincedeFlandreOrientale'
    else:
        return ""

#real estate
def RE_check(immo : str, zipcode : str, room : str, surface : str) -> str:
    result = ""
    if immo == "":
        result += "<br> Please choose a category <br/>"

    if zipcode == "":
        result += "<br> Please enter a zipcode <br/>"
    else:
        zipcode = int(zipcode)
        if zipcode < 1000 or zipcode > 9999:
            result += "<br> Please enter a plausible zipcode <br/>"

    if room == "":
        result += "<br> Please enter a number of room <br/>"

    else:
        room = int(room)
        if room < 1 or room > 100:
             result += "<br> Please enter a plausible number of room <br/>"


    if surface == "":
        result += "<br> Please enter a living area <br/>"

    else:
        surface = float(surface)
        if surface < 5 or surface > 1000:
            result += "<br> Please enter a plausible living area <br/>"

    return result

def models_loader() -> dict[str : any]:
    #get the all the file name in the model folder 
    models = {} 
    for file in os.listdir('models'):
        if file.endswith(".pickle"):
            name = file[:-7]
            print(name + " loaded")
            models[name] = pickle.load(open(f'models/{file}', 'rb'))

    return models


#############################################################################all pages functions
def menu(level : int) -> str : 

    if level == 0:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('login')}">Log In</a></li>
        <li><a href="{url_for('sign_up')}">Sign Up</a></li>
        """
        
    if level == 1:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('profile')}">My profile</a></li>
        <li><a href="{url_for('my_portfolio')}">My portfolio</a></li>
		<li><a href="{url_for('explorator')}">stocks explorator</a></li>
		<li><a href="{url_for('real_estate')}">Real estate</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """
    
    if level == 2:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('profile')}">My profile</a></li>
        <li><a href="{url_for('my_portfolio')}">My portfolio</a></li>
		<li><a href="{url_for('admin')}">admin panel</a></li>
		<li><a href="{url_for('churn')}">churn predictor</a></li>
        <li><a href="{url_for('explorator')}">stocks explorator</a></li>
		<li><a href="{url_for('real_estate')}">Real estate</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """
    
    if level == 3:

        return f"""
        <li><a href="{url_for('home')}">Home</a></li>
        <li><a href="{url_for('profile')}">My profile</a></li>
        <li><a href="{url_for('add_to_db')}">Add my files</a></li>
        <li><a href="{url_for('my_portfolio')}">My portfolio</a></li>
		<li><a href="{url_for('admin')}">admin panel</a></li>
		<li><a href="{url_for('churn')}">churn predictor</a></li>
        <li><a href="{url_for('explorator')}">stocks explorator</a></li>
		<li><a href="{url_for('real_estate')}">Real estate</a></li>
        <li><a href="{url_for('logout')}">Log out</a></li>      
        """

    return "Error attribution level"

############################################################################home pages functions
def buttons(level : int, username : str) -> str:
    if level == 0:

        return f"""

        <section>
        <h3 class="major">Where do you want to go?</h3>

        <ul class="actions fit">
			<li><a href="{url_for('login')}" class="button fit icon solid fa-user">Login</a></li>
			<li><a href="{url_for('sign_up')}" class="button fit icon solid fa-user-plus">Sign up</a></li>
		</ul>        
        </section>

        """

    if level == 1:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>

        <ul class="actions fit">
			<li><a href="{url_for('profile')}" class="button fit icon solid fa-id-card">My profile</a></li>
			<li><a href="{url_for('explorator')}" class="button fit icon solid fa-search">Stocks explorator</a></li>
		</ul>
		<ul class="actions fit">
			<li><a href="{url_for('real_estate')}" class="button fit icon solid fa-city">Real estate</a></li>
			<li><a href="{url_for('my_portfolio')}" class="button fit icon solid fa-table">My portfolio</a></li>
		</ul>
		<ul class="actions fit">
			<li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>       
        </section>

        """

    if level == 2:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>

        <ul class="actions fit">
			<li><a href="{url_for('profile')}" class="button fit icon solid fa-id-card">My profile</a></li>
			<li><a href="{url_for('explorator')}" class="button fit icon solid fa-search">Stocks explorator</a></li>
		</ul>
        <ul class="actions fit">
			<li><a href="{url_for('admin')}" class="button fit icon solid fa-chess-queen">Admin panel</a></li>
			<li><a href="{url_for('churn')}" class="button fit icon solid fa-people-arrows">Churn predictor</a></li>
		</ul>
		<ul class="actions fit">
			<li><a href="{url_for('real_estate')}" class="button fit icon solid fa-city">Real estate</a></li>
			<li><a href="{url_for('my_portfolio')}" class="button fit icon solid fa-table">My portfolio</a></li>
		</ul>
		<ul class="actions fit">
			<li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>       
        </section>

        """
    
    if level == 3:

        return f"""

        <section>
        <h3 class="major">Where do you want to go {username}?</h3>

        <ul class="actions fit">
			<li><a href="{url_for('profile')}" class="button fit icon solid fa-id-card">My profile</a></li>
			<li><a href="{url_for('explorator')}" class="button fit icon solid fa-search">Stocks explorator</a></li>
		</ul>
        <ul class="actions fit">
			<li><a href="{url_for('admin')}" class="button fit icon solid fa-chess-queen">Admin panel</a></li>
			<li><a href="{url_for('churn')}" class="button fit icon solid fa-people-arrows">Churn predictor</a></li>
		</ul>
		<ul class="actions fit">
			<li><a href="{url_for('real_estate')}" class="button fit icon solid fa-city">Real estate</a></li>
			<li><a href="{url_for('my_portfolio')}" class="button fit icon solid fa-table">My portfolio</a></li>
		</ul>
		<ul class="actions fit">
			<li><a href="{url_for('add_to_db')}" class="button fit icon solid fa-plus">Add my file</a></li>
            <li><a href="{url_for('logout')}" class="button fit icon solid fa-user-slash">Logout</a></li>
		</ul>       
        </section>

        """

    return "Error attribution level"

##################################################################admin & signup pages functions
def add_user(username : str, password : str, level : int) -> None:
    """Add a user to the database"""
    #encrypt the password wit hashlib
    password = hashlib.sha256(password.encode()).hexdigest() 
    #use engine_USR to add the user to the database
    engine_USR = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/users.db'), echo=False)
    conn_USR = engine_USR.connect()
    conn_USR.execute('INSERT INTO users (username, password, attr_level) VALUES (?, ?, ?)', (username, password, level), check_same_thread=False)
    conn_USR.close()

    return None


def check_user(username : str) -> bool:
    """Check if the user exists in the database"""   
    #use engine_USR to check if the user exists in the database
    engine_USR = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/users.db'), echo=False)
    conn_USR = engine_USR.connect()
    result = conn_USR.execute('SELECT * FROM users WHERE username = ?', (username)).fetchall()
    conn_USR.close()

    if len(result) == 0:
        return False

    return True

############################################################################login page functions
def loginf(username : str, password : str) -> bool:
    """check if username and password are correct"""
    password = hashlib.sha256(password.encode()).hexdigest() 
    #use engine_USR to check if the user exists in the database and get the password
    engine_USR = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/users.db'), echo=False)
    conn_USR = engine_USR.connect()
    #get result from the database where username = username and password = password
    result = conn_USR.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password), check_same_thread=False).fetchall()
    conn_USR.close()

    if len(result) == 0:
        return False
    
    return result[0][2]

##########################################################explorator & protfolio pages functions
def make_selector() -> str:
    """Make a selector of this type
    <input type = "text" list="company" placeholder="Company name">
		<datalist id="company">
		    <option value="Internet Explorer">
		</datalist>  """
    engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
    conn_FIN = engine_FIN.connect()
    #get the list of companies in the tickers table
    result = conn_FIN.execute('SELECT company FROM tickers').fetchall()
    conn_FIN.close()

    #make the selector
    selector = """
    
    <input type="text" list="company" id="cmp" name="company" />
		<datalist id="company">
    """
    for company in result:
        selector += f"""
        <option value="{company[0]}">
        """

    selector += """
    </datalist>
    """

    return selector
    
########################################################################multiple pages functions
def get_ticker(company : str) -> str:
    """Get the ticker of a company"""
    engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
    conn_FIN = engine_FIN.connect()
    #get the ticker of the company
    result = conn_FIN.execute('SELECT symbol FROM tickers WHERE company = ?', (company), check_same_thread=False).fetchall()
    conn_FIN.close()

    return result[0][0]

######################################################################explorator pages functions
def get_table(ticker : str) -> str:
    """make an html table from the data of a company"""

    engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
    conn_FIN = engine_FIN.connect()
    #get the data of the table ticker
    result = conn_FIN.execute(f'SELECT * FROM  "{ticker}"', check_same_thread=False).fetchall()
    conn_FIN.close()


    #make the table
    table = """
    <table class="alt">
    <tr>
        <th>Date</th>
        <th>Open</th>
        <th>High</th>
        <th>Low</th>
        <th>Close</th>
        <th>Adjusted Close</th>
        <th>Volume</th>
    </tr>
    """
    for row in result:
        table+=f"""
        <tr>
        """
        for col in row:
            table += f"""
            <td>{col}</td>
            """
        table += """
        </tr>
        """

    table += """
    </table>
    """

    return table


    

def get_graph(ticker : str) -> str:
    """make an html graph from the data of a company"""

    engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
    conn_FIN = engine_FIN.connect()
    #get the data of the table ticker
    result = conn_FIN.execute(f'SELECT * FROM  "{ticker}"', check_same_thread=False).fetchall()
    conn_FIN.close()

    #take 100 evenly spread data points
    result = result[::len(result)//250]

    #invert the data
    result = result[::-1]

    #make the graph using chart.js
    graph = f"""
    <canvas id="{ticker}" style="width:100%"></canvas>

        <script>
            const xValues = [
    """
    for row in result:
        graph += f"""
        '{row[0]}',
        """
    graph += """
    ]; 
    """



    graph +=f"""
            new Chart("{ticker}", """
    graph +="""{
                type: "line",
                    data: {
                        labels: xValues,
                        datasets: [{ 
                            data: ["""
    
    last = 0.0
    for row in result:
        try:
            last = float(row[1])
        except:
            pass
        graph += f"""{last},"""

    graph += """],
      borderColor: "red",
      fill: false
    }]
  },
  options: {
    legend: {display: false},
    title: {
      display: true,
      text: "stock prices over time",
      fontSize: 16
    }
    
  }
});
</script>
"""
    



    return graph



def get_graph_x(id : int, result) -> str:
    """make an html graph from the data of a company"""
    #take 100 evenly spread data points
    result = result[::len(result)//25]

    #invert the data
    result = result[::-1]

    #make the graph using chart.js

    script = f"""
    var ctx_{id} = document.getElementById('graph{id}').getContext('2d');
    var data_{id} = ["""
    last = 0.0
    for row in result:
        try:
            last = float(row[1])
        except:
            pass
        script += f"""{last},"""

    #remove the last comma
    script = script[:-1]

    script += f"""];

    var myChart_{id} = new Chart(ctx_{id},"""
    script += """{
        type: 'line',
        data: {
            labels: ["""
    for row in result:
        script += f"""'{row[0]}',"""

    #remove the last comma
    script = script[:-1]
    script += """],
            datasets: [{
                """
    script += f"""data: data_{id},"""
    script += """
                borderColor:"red",
                borderWidth: 1
            }]
        },
        options: {
    responsive: false
  }
});"""
                
    return script
    
###################################################################¼####portfolio page functions    
def get_table_limited(ticker : str, result) -> str:
    """make an html table from the data of a company"""

    

    #make the table
    table = """
    <table class="alt">
    <tr>
        <th>Date</th>
        <th>Open</th>
        <th>High</th>
        <th>Low</th>
        <th>Close</th>
        <th>Adjusted Close</th>
        <th>Volume</th>
    </tr>
    """
    for enumarate, row in enumerate(result):
        if enumarate == 10:
            break
        table+=f"""
        <tr>
        """
        for col in row:
            table += f"""
            <td>{col}</td>
            """
        table += """
        </tr>
        """

    table += """
    </table>
    """

    return table

def get_tickers(username : str) -> list:
    """get the tickers of the user from the followed db"""

    engine_FLD = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/followed.db'), echo=False)
    conn_FLD = engine_FLD.connect()
    #get the data of the table ticker
    result = conn_FLD.execute('SELECT ticker FROM followed WHERE username = ?', (username),  check_same_thread=False).fetchall()
    conn_FLD.close()

    return result

def add_ticker(username : str, ticker :str) -> None:
    """add a ticker to the followed db"""

    engine_FLD = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/followed.db'), echo=False)
    conn_FLD = engine_FLD.connect()
    #get the data of the table ticker
    conn_FLD.execute('INSERT INTO followed (username, ticker) VALUES (?, ?)', (username, ticker), check_same_thread=False)
    conn_FLD.close()

    return None

def get_company(ticker : str) -> str:
    """Get the company of a ticker"""
    engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
    conn_FIN = engine_FIN.connect()
    #get the ticker of the company
    result = conn_FIN.execute('SELECT company FROM tickers WHERE symbol = ?', (ticker), check_same_thread=False).fetchall()
    conn_FIN.close()

    return result[0][0]


#########################################################################add file page functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_file(filename : str) -> None:
    """add a file to the fin db"""

    engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
    conn_FIN = engine_FIN.connect()
    
    #put the data from the csv file into the db
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            conn_FIN.execute('INSERT INTO tickers (symbol, company) VALUES (?, ?)', (row[0], row[1]), check_same_thread=False)
            conn_FIN.execute(f'CREATE TABLE "{row[0]}" (date text, open real, high real, low real, close real, adj_close real, volume real)', check_same_thread=False)
            conn_FIN.execute(f'INSERT INTO "{row[0]}" (date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)', (row[2], row[3], row[4], row[5], row[6], row[7], row[8]), check_same_thread=False)
    conn_FIN.close()

    return None

								
################################################################################################							
@app.route('/')
def home():

    try:

        connected = session['connected'] 
        username = session['username']

    except: 

        session['connected'] : int = 0
        session['username'] : str = "Not connected"
        connected = session['connected'] 
        username = session['username']

    message = "Welcome! You are not connected."
    
    if connected == 1:
        message = f"Welcome {username}!"
    
    if connected == 2:
        message = f"Welcome {username}! You have employee privileges."
    
    if connected == 3:
        message = f"Welcome {username}! You have admin privileges."

    
    return render_template('index.html', 
                           Connected = username, 
                           menu = Markup(menu(connected)),
                           buttons = Markup(buttons(connected, username)),
                           message = message
                          )




################################################################################################
@app.route('/portfolio', methods = ['GET', 'POST'])
def my_portfolio():
    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    #if you are not connected
    if connected < 1:
        return home()




    if request.method == 'POST':

        try:
            company = request.form['company']
            ticker = get_ticker(company)
            add_ticker(username, ticker)
        except:
            print("Error during getting the company name")

    #get the list of tickers in the portfolio
    tickers = get_tickers(username)
    selector = make_selector()

    if tickers == []:
        return render_template(
            'portfolio.html',
            Connected = username,
            menu = Markup(menu(connected)),
            selector = Markup(selector),
            script = "",
            portfolio = "Your portfolio is empty"
        )

    

    script = """"""
    tables = ""
    #script = """<script>"""
    id = 1
    for ticker in tickers:
        try:

            engine_FIN = db.create_engine('sqlite:///' + os.path.join(basedir, 'databases/fin.db'), echo=False)
            conn_FIN = engine_FIN.connect()
            #get the data of the table ticker
            result = conn_FIN.execute(f'SELECT * FROM  "{ticker[0]}"', check_same_thread=False).fetchall()
            conn_FIN.close()


            #try:
            #    script += get_graph_x(id,result)
            #except Exception as e:
            #    print("Error during the graph creation")
            #    print(e)
            
            #tables+= f"""
            #<canvas id="graph{id}" style="width:100%"></canvas>
            #"""
            
            tables += f"""
            <h3>{get_company(ticker[0])}</h3>
            """
            
            tables += get_table_limited(ticker[0], result)
            tables += """
            <br>
            <br>
            """
            id += 1
        except:
            tables += f"""
            <h3>There is no data for {get_company(ticker[0])}</h3>
            <br>
            <br>
            """

    #script += """</script>"""


    return render_template(
        'portfolio.html',
        Connected = username,
        menu = Markup(menu(connected)),
        selector = Markup(selector),
        script = Markup(script),
        portfolio = Markup(tables)
    )

################################################################################################
@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    #if you are not connected & at least an admin
    if connected < 3:
         return home()
    
    if request.method == 'POST':

        if request.form['password'] != request.form['password2']:
            return render_template('admin.html', 
                                   wrong = "Passwords don't match", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        
        
        if check_user(request.form['username']):
            return render_template('admin.html', 
                                   wrong = "User already exists", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        


        attr_level = 1
        if request.form['attr_level'] == "Employee":
            attr_level = 2
        if request.form['attr_level'] == "Admin":
            attr_level = 3


        add_user(request.form['username'], request.form['password'], attr_level)

        return render_template('admin.html', 
                               wrong = "User added", 
                               Connected = username, 
                               menu = Markup(menu(connected)))



    return render_template('admin.html',
                            wrong = "",
                            Connected = username, 
                            menu = Markup(menu(connected)))

################################################################################################
@app.route('/churn', methods = ['GET', 'POST'])
def churn():
    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    #if you are not connected & at least an employee
    if connected < 2:
        return home()
    
    if request.method == 'POST':
        errors = ""
        r = ""

        #get the data from the form 
        if request.form['Client_ID'] == "" or request.form['Client_ID'] == None:
        
            try:
                Total_Relationship_Count = int(request.form['Total_Relationship_Count'])
            except:
                Total_Relationship_Count = 0
                errors += "Warning error during converting"

            try:
                Credit_Limit = float(request.form['Credit_Limit'])
            except:
                Credit_Limit = 0
                errors += "Warning error during converting"

            try:
                Total_Revolving_Bal = float(request.form['Total_Revolving_Bal'])
            except:
                Total_Revolving_Bal = 0
                errors += "Warning error during converting"

            try:
                Avg_Open_To_Buy = float(request.form['Avg_Open_To_Buy'])
            except:
                Avg_Open_To_Buy = 0
                errors += "Warning error during converting"

            try:
                Total_Trans_Amt = float(request.form['Total_Trans_Amt'])
            except:
                Total_Trans_Amt = 0
                errors += "Warning error during converting"

            try:
                Total_Trans_Ct = int(request.form['Total_Trans_Ct'])
            except:
                Total_Trans_Ct = 0
                errors += "Warning error during converting"

            data = pd.DataFrame({
            'Total_Relationship_Count': [Total_Relationship_Count],
            'Credit_Limit': [Credit_Limit],
            'Total_Revolving_Bal': [Total_Revolving_Bal],
            'Avg_Open_To_Buy': [Avg_Open_To_Buy],
            'Total_Trans_Amt' : [Total_Trans_Amt],
            'Total_Trans_Ct' : [Total_Trans_Ct]
            })

            #predict
            if clf.predict(data)[0] != 'Attrited Customer':
                r = 'not '  

            return render_template('churn.html',
                                   Connected = username,
                                   menu = Markup(menu(connected)),
                                   result=Markup(f"<h1> The client is {r}likely to churn </h1>") + errors)
        
        try:
            Client_ID = int(request.form['Client_ID'])
        except:
            Client_ID = 0
            errors += "Warning error during converting"


        
        data = data_CP.loc[data_CP['CLIENTNUM'] == Client_ID]

        if data.empty:
            return render_template('churn.html',
                                   Connected = username,
                                   menu = Markup(menu(connected)), 
                                   result=Markup(f"<h1> The client is not in the database </h1>"))

        if clf.predict(data)[0] != 'Attrited Customer':
            r = 'not '

        return render_template('churn.html',
                               Connected = username,
                               menu = Markup(menu(connected)), 
                               result=Markup(f"<h1> The client is {r}likely to churn </h1>") + errors)


    return render_template('churn.html', 
                           Connected = username, 
                           menu = Markup(menu(connected)),  
                           result=Markup(""))

################################################################################################
@app.route('/exploration', methods = ['GET', 'POST'])
def explorator():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    #if you are not connected
    if connected < 1:
        return home()
    
    selector = make_selector()

    if request.method == 'POST':

        try:
            company = request.form['company']
        except:
            print("Error during getting the company name")

        try:
            ticker = get_ticker(company)
        except:
            ticker = "No data available"

        table = f"""<h3>{company}: {ticker} data: </h3>"""


        try:
            table += get_table(ticker)
        except:
            table += "No data available"

        try:
            graph = get_graph(ticker)
        except:
            graph = ""

        return render_template('explorator.html',
                                Connected = username, 
                                menu = Markup(menu(connected)), 
                                selector = Markup(selector),
                                result = Markup(table),
                                graph = Markup(graph))


    
    
    return render_template('explorator.html',
                            Connected = username, 
                            menu = Markup(menu(connected)), 
                            selector = Markup(selector),
                            result = "",
                            graph = "")


################################################################################################
@app.route('/realestate', methods = ['GET', 'POST'])
def real_estate():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    #if you are not connected
    if connected < 1:
        return home()
    
    if request.method == 'POST':
        
        #category
        immo = request.form['category']
        #zipcode
        zipcode = request.form['zipcode']
        #number of room
        room = request.form['number of room']
        #living area
        surface = request.form['living Area']


        value : float = 0

        #check if the data are correct
        result : str = RE_check(immo, zipcode, room, surface)

        if result != "":
            return render_template('real_estate.html', 
                                   Connected = username, 
                                   menu = Markup(menu(connected)),  
                                   result=Markup(result))

        zipcode = int(zipcode)  

        room = int(room)

        surface = float(surface)

        #other usefull form field
        garden : str = request.form['Total Area of gardens']
        try:
            garden = float(garden)
        except:
            garden = 0

        terrace = request.form['Total Area of terraces']
        try:
            terrace = float(terrace)
        except:
            terrace = 0

    
        try:
            furnished = request.form['Furnished']
            if furnished == "on":
                furnished = True
            else:
                furnished = False
        except:
            furnished = False


        try:
            Equiped = request.form['Equiped kitchen']
            if Equiped == "on":
                Equiped = True
            else:
                Equiped = False
        except:
            Equiped = False




        name = RE_get_name(zipcode)
        try:
            current_mdl = models[name]
        except:
            return render_template('real_estate.html', 
                                   Connected = username, 
                                   menu = Markup(menu(connected)),  
                                   result=f"Sorry we don't have a model for {name}")

        if zipcode not in zipcode_converter.keys():
            return render_template('real_estate.html', 
                                   Connected = username, 
                                   menu = Markup(menu(connected)),  
                                   result=f"Sorry the zipcode: {zipcode} doesn't exist")
        zipcode_v = zipcode_converter[zipcode]

        if immo not in type_converter.keys():
            return render_template('real_estate.html', 
                                   Connected = username, 
                                   menu = Markup(menu(connected)),  
                                   result=f"Sorry the type: {immo} doesn't exist")
        immo_v = type_converter[immo]

        if zipcode not in tax_converter:
            return render_template('real_estate.html', 
                                   Connected = username, 
                                   menu = Markup(menu(connected)), 
                                   result=f"Sorry the zipcode: {zipcode} doesn't refer to a city tax")
        tax = tax_converter[zipcode]


        #make a dict of the data
        data = {
                'Number of rooms': room, 
                'Living Area': surface, 
                'Fully equipped kitchen': Equiped, 
                'Furnished': furnished, 
                'Area of the terrace': terrace,
                'Area of the garden': garden, 
                'zipcode': zipcode_v,    
                'type': immo_v, 
                'Taxe': tax
            }

        #transform the dict in a data frame
        data = pd.DataFrame(data, index=[0])

        value = current_mdl.predict(data)*surface
        value = round(value[0])

        #save to log
        with open('log.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()} : {immo} {zipcode} {room} {surface} {garden} {terrace} {furnished} {Equiped} {value}\n")

        return render_template('real_estate.html', 
                               Connected = username, 
                               menu = Markup(menu(connected)),
                               result=f"Your {immo} has a value of approximatly {value} euros. (The selected model is XGboost{name})")


    
    return render_template('real_estate.html', 
                           Connected = username, 
                           menu = Markup(menu(connected)),
                           result="")

################################################################################################
@app.route('/add_to_db' , methods = ['GET', 'POST'])
def add_to_db():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    #if you are not Admin
    if connected < 3:
        return home()
    
    if request.method == 'POST':
    
        #get the file
        file = request.files['file']
        #get the name of the file
        filename = file.filename
        #get the extension of the file
        ext = filename.split('.')[-1]
        #check if the extension is csv
        if ext != 'csv':
            return render_template('addfile.html',
                                    Connected = username, 
                                    menu = Markup(menu(connected)),
                                    message="The file must be a csv")
        
        #save the file in the folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #add the file to the database
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            add_file(filename)
        except:
            return render_template('addfile.html',
                                    Connected = username, 
                                    menu = Markup(menu(connected)),
                                    message="Problem with the file")
        
        return render_template('addfile.html',
                                Connected = username,
                                menu = Markup(menu(connected)),
                                message="The file has been added to the database")


    return render_template('addfile.html',
                            Connected = username, 
                            menu = Markup(menu(connected)),
                            message="")

################################################################################################
@app.route('/profile')
def profile():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    if connected < 1:
        return home()
    
    att = "Unknown"
    if connected == 1:
        att = "User"

    if connected == 2:
        att = "Employee"

    if connected == 3:
        att = "Admin"


    tickers = get_tickers(username)
    companies = "<h2>Companies you follow</h2>"
    for ticker in tickers:
        companies += f"""
                            <h3>{get_company(ticker[0])} : {ticker[0]}</h3>
                            
                      """
        
    if ticker == "":
        companies = "<h2>You don't follow any company</h2>"

    return render_template('user.html', 
                           Connected = username, 
                           menu = Markup(menu(connected)),
                           user=Markup(f"""<h1>Hello {username}!</h1>
                                           <h2>You're attribution level is {connected} which correspond to the {att} level.</h2>""" + companies))

################################################################################################
@app.route('/login' , methods = ['GET', 'POST'])
def login():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    if connected > 0:
        return home()

    if request.method == 'POST':
        user = request.form['id']
        password = request.form['password']

        attr = loginf(user, password)

        if attr:
            session['connected'] = attr
            session['username'] = user
            return home()
        
        return render_template('login.html',
                                Connected = username, 
                                menu = Markup(menu(connected)),
                                wrong = "Wrong id or password")
    
    return render_template('login.html',
                            Connected = username, 
                            menu = Markup(menu(connected)),
                            wrong = "")

################################################################################################
@app.route('/signup', methods = ['GET', 'POST'])
def sign_up():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()
    
    if connected > 0:
        return home()
    
    if request.method == 'POST':
        
        if request.form['password'] != request.form['password2']:
            return render_template('signup.html', 
                                   wrong = "Passwords don't match", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        
        
        if check_user(request.form['username']):
            return render_template('signup.html', 
                                   wrong = "User already exists", 
                                   Connected = username, 
                                   menu = Markup(menu(connected)))
        


        attr_level = 1
        if request.form['attr_level'] == "Employee":
            attr_level = 2
        if request.form['attr_level'] == "Admin":
            attr_level = 3
        
                

        session['connected'] = attr_level
        session['username']= request.form['username']


        add_user(request.form['username'], request.form['password'], attr_level)
        return home()


    if session['connected'] == 0:
        return render_template('signup.html', 
                               Connected = username, 
                               menu = Markup(menu(connected)))
    
    return home()

################################################################################################
@app.route('/logout')
def logout():

    try:
        connected = session['connected'] 
        username = session['username']
    except:
        return home()

    if session['connected'] == 0:
        return home()
    
    session['connected'] = 0
    session['username']= "Not connected"

    return render_template('logout.html')




################################################################################################
#data for real estate prediction
data_RE : pd.DataFrame = pd.read_csv(os.path.join(basedir, 'data/data_for_regression.csv'))
#prepare the data
zipcode_converter : dict[int:float] = RE_prepare_zipcode(data_RE)
tax_converter : dict[int:float] = RE_prepare_tax(data_RE)
type_converter : dict[str:float] = RE_prepare_type(data_RE)

#load the data for the churn prediction
database = os.path.join(basedir, 'databases/churn.db')
conn = sqlite3.connect(database)
data_CP : pd.DataFrame = pd.read_sql('SELECT CLIENTNUM, Attrition_Flag, Total_Relationship_Count, Credit_Limit, Total_Revolving_Bal, Avg_Open_To_Buy, Total_Trans_Amt, Total_Trans_Ct FROM bank_churners', conn)
conn.close()

database = os.path.join(basedir, 'databases/fin.db')
userbase = os.path.join(basedir, 'databases/users.db')

conn_FIN = sqlite3.connect(database)

#load machine learning models
# for churn prediction 
# and real estate prediction
models : dict[str:any] = models_loader()
clf = models['churn_model']

serve(app, host="0.0.0.0", port=8080)
app.run(debug=False)