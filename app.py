#importing
# import *file name
# import from file name import what you want 
from flask import Flask,render_template,request,redirect,url_for

import pygal
import psycopg2

from flask_sqlalchemy import SQLAlchemy

from config.config import Development,Production
# specific
# from pygal import pie

# calling/instanciating
app = Flask(__name__)
# load configuration
app.config.from_object(Development)
# database://user:password@host:port/databasename

# calling/instanciating of Sqlalchemy
# comes with helpers and functions
db = SQLAlchemy(app)

# creating tables
from Model.inventory import InventoryModel
from Model.stock import StockModel
from Model.sales import SalesModel

@app.before_first_request
def create_tables():
    db.create_all()

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
    inventories=InventoryModel.query.all()
    print(inventories)


    if request.method =='POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price'] 
 
        # print(name)
        # print(inv_type)
        # print(buying_price)
        # print(selling_price)

        new_inv = InventoryModel(name=name,inv_type=inv_type, buying_price=buying_price,selling_price=selling_price)
        new_inv.add_inventories()
        
        return redirect (url_for('inventories')) 

    return render_template('inventories.html', inventories=inventories)

@app.route('/add_stock/<inv_id>', methods=['POST'])
def add_stock(inv_id):
    # print(inv_id)

    if request.method == 'POST':
        stock = request.form['stock']
        new_stock = StockModel(inv_id=inv_id, quantity=stock)
        new_stock.add_stock()

        return redirect (url_for('inventories'))  



@app.route('/add_sale/<inv_id>',methods=['POST'])
def add_sale(inv_id):
    print(inv_id)
    if request.method =='POST':
        sale = request.form['sale']
        new_sale = SalesModel(inv_id=inv_id, quantity=sale)
        new_sale.add_sale()
        # sale = request.form['sale']
        # print(sale)

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
    conn = psycopg2.connect("dbname='postgres' user= 'postgres' host='localhost' port='5432' password='kiprugut'")

    cur = conn.cursor()
    cur.execute(""" 
    SELECT type,count(type)
	FROM public.inventories
	
	GROUP BY type
    
    """)
    product_service = cur.fetchall()

    print(product_service)

    # initializing your pie chart
    
    pie_chart= pygal.Pie()
    # my_pie_data = [
    #     ('Nairobi',40),
    #     ('Kilifi' ,10),
    #     ('Machakos' ,10),
    #     ('Kiambu' ,20),
    #     ('Nakuru',20)
    #     ]

         
    pie_chart.title ='FRUITS AND VEGETABLES'
    for each in product_service:
        pie_chart.add(each[0],each[1])

    pie_data = pie_chart.render_data_uri()
    
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
    cur.execute("""
    SELECT EXTRACT(MONTH FROM s.created_at)as sales_month,sum (quantity  * selling_price) as total_sales
	FROM sales as s
	join inventories as i on s.inv_id=i.id
	group by sales_month
	order by sales_month asc;
    

    """)

    monthly_sales=cur.fetchall()
    # print(monthly_sales)

    # data = [
    #      {'month':'January','total':22},
    #      {'month':'February','total':27},
    #      {'month':'March','total':23},
    #      {'month':'April','total':20},
    #      {'month':'May','total':12},
    #      {'month':'June','total':32},
    #      {'month':'July','total':42},
    #      {'month':'August','total':72},
    #      {'month':'September','total':52},
    #      {'month':'October','total':42},
    #      {'month':'November','total':92},
    #      {'month':'December','total':102}
    #  ]

    a=[]
    b=[]
    for each in  monthly_sales :
        #   print(monthly_sales)
          
        x=each[0]
        y=each[1]
        a.append(x)
        b.append(y)

    

    line_chart = pygal.Line()
    line_chart.title = 'MONTHLY SALES'
    line_chart.x_label = a
    line_chart.add('Monthly Sales',b)
      
         

    # line_chart.add('Firefox',[None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    # line_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    # line_chart.add('IE', [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    # line_chart.add('Others',[14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

    line_data = line_chart.render_data_uri()

    return render_template('charts.html',chart=pie_data,line=line_data)

#  run_your_app
if __name__=="__main__":
    app.run()