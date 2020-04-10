#importing
# import *file name
# import from file name import what you want 
from flask import Flask,render_template,request,redirect,url_for

import pygal
import psycopg2
# specific
# from pygal import pie

# calling/instanciating
app = Flask(__name__)

# creating of endpoints/route
# 1. declaration of a route 
@app.route('/')
 # 2.a function embedded to the route
def hello_world():
     return '<h1>Welcome to web development </h1>'

# @app.route('/home')
# def home():
#     return 'welcome to my homepage'

# @app.route('/about')
# def about():
#     return 'welcome to our about page'

# @app.route('/contact_us')
# def contact_us():
#     return 'contact us'

# @app.route('/services')
# def services():
#     return ' our services' 

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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/service')
def service():
    return render_template('service.html') 

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/aboutt')
def aboutt():
    return render_template('about.html')           

@app.route('/inventories', methods=['GET', 'POST'])
def inventories():


    if request.method =='POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price'] 
 
        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)
        return redirect (url_for('inventories')) 

    return render_template('inventories.html')

@app.route('/add_stock',methods=['POST'])
def add_stock():
    if request.method == 'POST':
        stock = request.form['stock']
        print(stock) 

        return redirect (url_for('inventories'))   


@app.route('/add_sale',methods=['POST'])
def add_sale():
    if request.method =='POST':
        sale = request.form['sale']
        print(sale)

        return redirect(url_for('inventories'))

@app.route('/edit_inventory',methods=['POST'])
def edit_inventory():
    if request.method == 'POST':

        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']


        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)

        return redirect(url_for('inventories'))


@app.route('/data_visualisation')
def data_visualisation():
    # conn = psycopg2.connect("dbname='postgres' user= 'postgres' host='localhost' port='5432' password='kiprugut'")

    # cur = conn.cursor()
    # cur.execute(""" 
    # SELECT type,count(type)
	# FROM public.inventories
	
	# GROUP BY type
    
    # """)
    # product_service = cur.fetchall()

    # print(product_service)

    # initializing your pie chart
    
    pie_chart= pygal.Pie()
    my_pie_data = [
        ('Nairobi',40),
        ('Kilifi' ,10),
        ('Machakos' ,10),
        ('Kiambu' ,20),
        ('Nakuru',20)
        ]

    
    for each in my_pie_data:
        pie_chart.add(each[0],each[1])

        pie_data = pie_chart.render_data_uri()     
    pie_chart.title ='Total Sales'
    print(my_pie_data)
    # add components to your pie chart
        # 1.add title
        # 2.partition your pie chart

    
    # pie_chart.add('Nairobi',40)
    # pie_chart.add('Kilifi',10)
    # pie_chart.add('Machakos',10)
    # pie_chart.add('Kiambu',20)
    # pie_chart.add('Nakuru',20)
    # end of piechart

    # start of line_chart
    # cur.execute("""
    
    
    
    # """)

    #  monthly_sales=cur.fetchall()
    #  print(monthly_sales)

    data = [
         {'month':'January','total':22},
         {'month':'February','total':27},
         {'month':'March','total':23},
         {'month':'April','total':20},
         {'month':'May','total':12},
         {'month':'June','total':32},
         {'month':'July','total':42},
         {'month':'August','total':72},
         {'month':'September','total':52},
         {'month':'October','total':42},
         {'month':'November','total':92},
         {'month':'December','total':102}
     ]
    a=[]
    b=[]
    for each in data:

        x=each["month"]
        y=each["total"]
        a.append(x)
        b.append(y)


        line_chart = pygal.Line()
        line_chart.title = 'MONTHLY SALES'
        line_chart.x_label = a
        line_chart.add('MonthlySales',b)
        print(data)
         

    # line_chart.add('Firefox',[None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    # line_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    # line_chart.add('IE', [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    # line_chart.add('Others',[14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

        line_data = line_chart.render_data_uri()

        return render_template('charts.html',chart=pie_data,line=line_data)

#  run_your_app
if __name__=="__main__":
    app.run()