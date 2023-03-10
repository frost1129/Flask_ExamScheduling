import os.path
import string

from schedule_app import app
from flask import render_template, request, redirect, url_for


@app.route('/', methods=['GET', 'POST'])
def home():
    uploaded_file = os.listdir(app.config['UPLOAD_FOLDER'])
    file_name = None

    for file in uploaded_file:
        file_name = file

    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return render_template('index.html', message='Không tìm thấy file CSV!', cue='warning', file_name=file_name)

        csv_file = request.files['csv_file']

        # Kiểm tra xem file csv có trống hay không
        if csv_file.filename == '':
            return render_template('index.html', message='Vui lòng chọn file CSV', cue='warning', file_name=file_name)

        # Lưu file vào uploads
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_file.filename)
        csv_file.save(file_path)
        file_name = csv_file.filename

        return render_template('index.html', message='Tải file lên thành công', cue='success', file_name=file_name)

    return render_template('index.html', file_name=file_name)


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    # Lấy data từ coloring
    # Hiển thị dữ liệu

    return render_template('schedule.html')


@app.route('/delete-csv/<filename>', methods=['POST'])
def delete_csv(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html', message='Xóa file thành công!', cue='success')


if __name__ == '__main__':
    app.run(debug=True)
