#importing
# import *file name
# import from file name import what you want 
from flask import Flask,render_template,request,redirect,url_for,flash
from werkzeug.middleware.shared_data import SharedDataMiddleware

import pygal
import psycopg2


from flask_sqlalchemy import SQLAlchemy

from config.config import Production
# specific
# from pygal import pie

# calling/instanciating
app = Flask(__name__)

app.add_url_rule('/uploads/<img1>', 'uploaded_file', build_only=True)

# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/uploads':  app.config['UPLOAD_FOLDER']})



# load configuration
app.config.from_object(Production)
# database://user:password@host:port/databasename

# calling/instanciating of Sqlalchemy
# comes with helpers and functions
db = SQLAlchemy(app)

# to run locally/development psycopg2 connection
# conn = psycopg2.connect("dbname='postgres' user= 'postgres' host='localhost' port='5432' password='kiprugut'")

# to run from heroku/production psycopg2 connection
conn = psycopg2.connect("dbname='d83hg5c2ovh1dq' user= 'abggqjxxipfojm' host='ec2-52-201-55-4.compute-1.amazonaws.com' port='5432' password='5af7d9ea18038e18bcecd21bad73727573c79d67bb0c9671a768883eb789e19e'")
cur = conn.cursor()

# creating tables
from Model.inventory import InventoryModel
from Model.stock import StockModel
from Model.sales import SalesModel

# decorators
@app.before_first_request
def create_tables():
    db.create_all()



# creating of endpoints/route
# 1. declaration of a route 
@app.route('/')
 # 2.a function embedded to the route
def homepage():
     return render_template('homepage.html')
  

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


# multiplication
@app.route('/mul/<a>/<b>')
def mul(a,b):
        mul=int(a)*int(b)
        return str(mul)


# division
@app.route('/div/<a>/<b>')
def div(a,b):
        div=int(a)/int(b)
        return str(div)        


# concutination using f string
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

    # print(inventories)
    cur.execute("""   
SELECT inv_id, sum(quantity) as "remaining_stock" 		
FROM (SELECT st.inv_id, sum(quantity) as "quantity" 		
FROM public.new_stock as st 		
GROUP BY inv_id 
	  
	  union all 
	  
SELECT sa.inv_id, - sum(quantity) as "quantity" 	
FROM public.new_sales as sa 		
GROUP BY inv_id) as stsa 		
GROUP BY inv_id 		

ORDER BY inv_id;
        """ )

    remaining_stock=cur.fetchall()



    if request.method =='POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price'] 
 
        # print(name)
        # print(inv_type)
        # print(buying_price)
        # print(selling_price)

        '''
        STEPS TO INSERT RECORDS
        1.create yyour model object
        '''
        # insert records 
        new_inv = InventoryModel(name=name,inv_type=inv_type, buying_price=buying_price,selling_price=selling_price)
        new_inv.add_inventories()

        # flash('Inventory added successfully' ,'warning')

        # InventoryModel.add_inventories(new_inv)
        return redirect (url_for('inventories')) 

    return render_template('inventories.html', inventories=inventories,remaining_stock=remaining_stock)

@app.route('/add_stock/<inv_id>', methods=['POST'])
def add_stock(inv_id):
    # print(inv_id)

    if request.method == 'POST':
        stock = request.form['stock']
        new_stock = StockModel(inv_id=inv_id, quantity=stock)
        new_stock.add_stock()

        return redirect (url_for('inventories'))  



@app.route('/add_sale/<inv_id>', methods=['POST'])
def add_sale(inv_id): 
    print(inv_id)
    if request.method =='POST':
    
        sale= request.form['quantity']
        new_sale = SalesModel(inv_id=inv_id, quantity=sale)
        new_sale.add_sale()
        # sale = request.form['sale']
        # print(sale)

        return redirect(url_for('inventories'))



@app.route('/edit_inventory/<inv_id>',methods=['GET','POST'])
def edit_inventory(inv_id):

    record = InventoryModel.query.filter_by(id=inv_id).first()


    if request.method == 'POST':


        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']

        if record:
            record.name = name
            record.inv_type = inv_type
            record.buying_price = buying_price
            record.selling_price = selling_price

            db.session.commit()

        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)



        return redirect(url_for('inventories',inv))

@app.route('/view_sales/<inv_id>')
def view_sales(inv_id):
    sales = SalesModel.get_sales_by_id(inv_id)
    inv_name=InventoryModel.query.filter_by(id=inv_id).first()
    return render_template('viewsales.html', sales=sales,inv_id=inv_id, inv_name=inv_name)

@app.route('/delete/<inv_id>')
def delete_inventory(inv_id):
    record = InventoryModel.query.filter_by(id=inv_id).first()
    
    if record:
        db.session.delete(record)
        db.session.commit()

    else:
        print("None existance")

        flash('record deleted')


    return redirect(url_for('inventories'))



@app.route('/data_visualisation')
def data_visualisation():
    
    cur.execute(""" 
    SELECT inv_type,count(inv_type)
	FROM public.new_inventories
	
	GROUP BY inv_type
    
    """)
    product_service = cur.fetchall()

    print(product_service)



    # initializing your pie chart
    
    pie_chart= pygal.Pie()
    '''

    my_pie_data = [
        ('Nairobi',40),
        ('Kilifi' ,10),
        ('Machakos' ,10),
        ('Kiambu' ,20),
        ('Nakuru',20)
        ]

'''
         
    pie_chart.title ='PRODUCT AND SERVICES'
    for each in product_service:
        pie_chart.add(each[0],each[1])

    pie_data = pie_chart.render_data_uri()

    '''
    add components to your pie chart
        1.add title
        2.partition your pie chart

    
    pie_chart.add('Nairobi',40)
    pie_chart.add('Kilifi',10)
    pie_chart.add('Machakos',10)
    pie_chart.add('Kiambu',20)
    pie_chart.add('Nakuru',20)

'''
    # end of piechart

    # start of line_chart
    cur.execute("""
   SELECT EXTRACT(MONTH FROM s.created_at)as new_sales_month,sum (quantity  * selling_price) as total_new_sales
	FROM new_sales as s
	join new_inventories as i on s.inv_id=i.id
	group by new_sales_month
	order by new_sales_month asc;
    

    """)

    new_monthly_sales=cur.fetchall()
    # print(new_monthly_sales)

    a=[]
    b=[]
    for each in  new_monthly_sales :
        #  print(monthly_sales)
          
        x=each[0]
        y=each[1]

        a.append(x)
        b.append(y)

        line_chart = pygal.Line()
        line_chart.title = 'MONTHLY SALES'
        line_chart.x_label = a
        line_chart.add('Monthly Sales',b)

        
        line_data = line_chart.render_data_uri()


    return render_template('charts.html',chart=pie_data,line=line_data)
      
         
'''
    line_chart.add('Firefox',[None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',[14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
'''


      

#  run_your_app
if __name__=="__main__":
    app.run()