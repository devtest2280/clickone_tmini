from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///counter.db'
db = SQLAlchemy(app)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    counter = Counter.query.first()
    if counter:
        return render_template('index.html', counter=counter.value)
    else:
        counter = Counter(value=0)
        db.session.add(counter)
        db.session.commit()
        return render_template('index.html', counter=counter.value)

@app.route('/increment')
def increment():
    counter = Counter.query.first()    
    return str(counter.value)

@app.route('/update', methods=['POST'])
def update():
    counter_value = request.json['counter']
    counter = Counter.query.first()
    if counter:
        counter.value = counter_value
    else:
        counter = Counter(value=counter_value)
        db.session.add(counter)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
