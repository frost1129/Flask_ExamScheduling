import os.path

from schedule_app import app, db, CSVFile
from flask import render_template, request


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        csv_files = CSVFile.query.all()
        if 'csv_file' not in request.files:
            return render_template('index.html', message='Không tìm thấy file CSV!', cue='warning', csv_files=csv_files)

        csv_file = request.files['csv_file']

        # Kiểm tra xem file csv có trống hay không
        if csv_file.filename == '':
            return render_template('index.html', message='Vui lòng chọn file CSV', cue='warning', csv_files=csv_files)

        if CSVFile.query.filter_by(name=csv_file.filename).first() is not None:
            return render_template('index.html', message='File đã tồn tại, không thể tải file trùng lấp!', cue='warning', csv_files=csv_files)

        # Lưu file vào uploads
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
        csv_file.save(file_path)

        # Lưu nội dung file vào csdl:
        with open(file_path, 'rb') as f:
            csv_content = f.read()
        new_csv = CSVFile(name=csv_file.filename, data=csv_content)

        db.session.add(new_csv)
        db.session.commit()

        # load danh sách các file đã tải lên
        csv_files = CSVFile.query.all()
        return render_template('index.html', message='Tải file lên thành công', cue='success', csv_files=csv_files)

    # GET
    csv_files = CSVFile.query.all()

    return render_template('index.html', csv_files=csv_files)


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        if request.form.get("csv_file"):
            return 'Success'

        # Nếu chưa chọn file muốn xử lý
        csv_files = CSVFile.query.all()
        return render_template('index.html', message='Vui lòng chọn file dữ liệu', cue='warning', csv_files=csv_files)

    return 'Nothing happen!'


@app.route('/delete-csv/<int:csv_id>', methods=['POST'])
def delete_csv(csv_id):
    # Xác định đối tượng CSVFile theo ID
    csv_file = CSVFile.query.filter_by(id=csv_id).first()

    if csv_file:
        # Xóa file CSV
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.name)
        os.remove(file_path)

        # Xóa đối tượng CSVFile khỏi cơ sở dữ liệu
        db.session.delete(csv_file)
        db.session.commit()

        # Trả về thông báo xóa file thành công
        csv_files = CSVFile.query.all()
        return render_template('index.html', message='Xóa file thành công!', cue='success', csv_files=csv_files)
    else:
        # Trả về thông báo không tìm thấy file
        csv_files = CSVFile.query.all()
        return render_template('index.html', message='Không tìm thấy file!', cue='warning', csv_files=csv_files)


if __name__ == '__main__':
    app.run(debug=True)
