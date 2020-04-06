#importing
# import *file name
# import from file name import what you want 
from flask import Flask,render_template

# calling/instanciating
app = Flask(__name__)

# creating of endpoints/route
# 1. declaration of a route 
@app.route('/')

# 2.a function embedded to the route
def hello_world():
    return '<h1>Welcome to web development </h1>'

@app.route('/home')
def home():
    return 'welcome to my homepage'

@app.route('/about')
def about():
    return 'welcome to our about page'

@app.route('/contact_us')
def contact_us():
    return 'contact us'

@app.route('/services')
def services():
    return ' our services' 

@app.route('/name/<name>')
def my_name():
    return f'My name is {my_name}'
    # return 'my name is{}'.format(name)
    # return 'My name is '+name

# sum two numbers dynamically
@app.route('/sum/<a>/<b>')
def sum(a,b):
        sum=int(a)+int(b)
        return str(sum)
    # return a,b

@app.route('/mul/<a>/<b>')
def mul(a,b):
        mul=int(a)*int(b)
        return str(mul)

@app.route('/div/<a>/<b>')
def div(a,b):
        div=int(a)/int(b)
        return str(div)        


@app.route('/my_story/<name>/<age>/<town>')
def my_story(name,age,town):
    return f'my name is{name}.i am {age} from {town}town.'

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/service')
def service():
    return render_template('service.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/aboutt')
def aboutt():
    return render_template('aboutt.html')           

@app.route('/inventories1')
def inventories1():
    return render_template('inventories1.html')

#  run_your_app
if __name__=="__main__":
    app.run()