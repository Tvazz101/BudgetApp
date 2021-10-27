from flask import Flask,render_template,url_for,request,redirect, session
from sqlalchemy.sql.functions import current_date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime
app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_9.db'
db = SQLAlchemy(app)
app.secret_key = "Savage"


numby = 1

# All of the classes
class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime(), nullable= False)
    end_date = db.Column(db.DateTime(), nullable=False)
    deposits = db.relationship('Deposit', backref='author', lazy=True)
    bills = db.relationship('Bill', backref='biller', lazy=True)
    transactions = db.relationship('Transaction', backref='payer', lazy=True)
    investments = db.relationship('Investment', backref='investor', lazy=True)


    def __repr__(self):
        return f'Budget Period for id ID#{self.id} created'


class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.today())
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Deposit for ID#{self.id} created'

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.today())
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), default="U")
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)

    def __repr__(self):
        return f'Bill for ID#{self.id} created'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.today())
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20))
    description = db.Column(db.String(100))
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)

    def __repr__(self):
        return f'Transaction for ID#{self.id} created'

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.today())
    amount = db.Column(db.Integer, nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)

    def __repr__(self):
        return f'Investment for ID#{self.id} created'




# All of the routes
@app.route('/set_budget', methods=['POST', 'GET'])
def set_budget():
    if request.method == 'POST':
        budget_number = request.form['budget_number']
        session["period"] = budget_number
        return redirect('/')

        


    else:

        return render_template('set_budget.html')

@app.route('/test1', methods=['Get'])
def learning():
    numby=+1
    return f"<h1>Hello World {numby}</h1>"
        
@app.route('/', methods=['POST', 'GET'])
def home():
    
    if request.method == 'POST':
        
     return redirect('/Prepurchase')
        
    


    else:
        
        current_date = datetime.datetime.today()
        cycle = Period.query.all()
        current_period = cycle[-1]
        start_time = current_period.start_date
        end_time = current_period.end_date
        days_added = datetime.timedelta(days=14)
        new_week = current_date + datetime.timedelta(days=14)
        
        
        
        if start_time <= current_date <= end_time:
          
            
            number = current_period.id
            periods = Period.query.order_by(Period.id).all()
            bills = Bill.query.filter_by(period_id=number).order_by(Bill.id).all()
            bill_total = db.session.query(db.func.sum(Bill.amount)).filter_by(period_id=number).scalar()
            deposits = Deposit.query.order_by(Deposit.id).filter_by(period_id=number).all()
            deposit_total = db.session.query(db.func.sum(Deposit.amount)).filter_by(period_id=number).scalar()
            transactions = Transaction.query.filter_by(period_id=number).order_by(Transaction.id).all()
            savings_total = db.session.query(db.func.sum(Investment.amount)).scalar()
            savings_deposits = Investment.query.filter_by(period_id=number).order_by(Investment.id).all()

            start_text = current_period.start_date.strftime('%B %d, %Y')
            end_text = current_period.end_date.strftime('%B %d, %Y')
        
                
            return render_template('home_page.html', periods=periods, bills=bills,bill_total=bill_total,
                                            transactions=transactions, deposits=deposits,
                                             deposit_total=deposit_total, savings_total=savings_total,
                                             savings_deposits=savings_deposits, current_period=current_period,
                                             start_text=start_text, end_text=end_text,)
                    
        else:
            new_period = Period(start_date=current_date, end_date=new_week)
            db.session.add(new_period)
            db.session.commit()
            return redirect("/")
        

@app.route('/Prepurchase', methods=['GET'])
def Prepurchase():

    return render_template('Prepurchase.html')

@app.route('/Add_bill', methods=['POST', 'GET'])
def add_bill():
    if request.method == 'POST':
        bill = request.form['bill_amount']
        cycle = Period.query.all()
        current_period = cycle[-1]
        new_bill = Bill(amount=bill, period_id=current_period.id)

        try:
            db.session.add(new_bill)
            db.session.commit()
            return redirect("/")

        except:
            return 'There was an issue adding your bill Taj'


    else:

        return render_template('Add_bill.html')


@app.route('/Add_transaction', methods=['POST', 'GET'])
def add_purchase():
    if request.method == 'POST':
        purchase = request.form['purchase_amount']
        cycle = Period.query.all()
        current_period = cycle[-1]
        new_purchase = Transaction(amount=purchase, period_id=current_period.id)

        try:
            db.session.add(new_purchase)
            db.session.commit()
            return redirect("/")

        except:
            return 'There was an issue adding your bill Taj'


    else:

        return render_template('Add_transaction.html')

@app.route('/Add_deposit', methods=['POST', 'GET'])
def add_deposit():
    if request.method == 'POST':
        deposit = request.form['deposit_amount']
        cycle = Period.query.all()
        current_period = cycle[-1]
        new_deposit = Deposit(amount=deposit, period_id=current_period.id)

        try:
            db.session.add(new_deposit)
            db.session.commit()
            return redirect("/")

        except:
            return 'There was an issue adding your bill Taj'


    else:

        return render_template('Add_deposit.html')

@app.route('/Add_savings', methods=['POST', 'GET'])
def add_savings():
    if request.method == 'POST':
        investment = request.form['savings_amount']
        cycle = Period.query.all()
        current_period = cycle[-1]
        new_investment = Investment(amount=investment, period_id=current_period.id)

        try:
            db.session.add(new_investment)
            db.session.commit()
            return redirect("/")

        except:
            return 'There was an issue adding your bill Taj'


    else:

        return render_template('Add_savings.html')


@app.route('/review_pages', methods=['GET', 'POST'])
def reviewList():
    if request.method == "POST":
        budget_number = request.form['Budget_ID']
        session["period"] = budget_number
        return redirect('/reviewed_pages')

    
    else:
        periods = Period.query.order_by(Period.id).all()
        return render_template('Review_pages.html', periods=periods)

@app.route('/delete_budget_week')
def delete_budget_week():
    cycle = Period.query.all()
    deleted_period = cycle[-1]
    db.session.delete(deleted_period)
    db.session.commit()
    return redirect('/')

@app.route('/adding_new_week')
def adding_new_week():
    new_date = datetime.datetime.today()
    new_week = new_date + datetime.timedelta(days=14)
    new_period = Period(start_date=new_date, end_date=new_week)
    db.session.add(new_period)
    db.session.commit()
    return redirect('/Add_bill')

@app.route('/reviewed_pages', methods=['GET', 'POST'])
def reviewdPage():
    number = session['period']
    periods = Period.query.order_by(Period.id).all()
    bills = Bill.query.filter_by(period_id=number).order_by(Bill.id).all()
    bill_total = db.session.query(db.func.sum(Bill.amount)).filter_by(period_id=number).scalar()
    deposits = Deposit.query.order_by(Deposit.id).filter_by(period_id=number).all()
    deposit_total = db.session.query(db.func.sum(Deposit.amount)).filter_by(period_id=number).scalar()
    transactions = Transaction.query.filter_by(period_id=number).order_by(Transaction.id).all()
    savings_total = db.session.query(db.func.sum(Investment.amount)).scalar()
    savings_deposits = Investment.query.filter_by(period_id=number).order_by(Investment.id).all()
        
    return render_template('home_page.html', periods=periods, bills=bills,bill_total=bill_total,
                                    transactions=transactions, deposits=deposits,
                                        deposit_total=deposit_total, savings_total=savings_total,
                                        savings_deposits=savings_deposits)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


