from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = '*&#*%^#@@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456abc@localhost/exam_csv?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # Giới hạn kích thước file là 16MB

db = SQLAlchemy(app)


class CSVFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
