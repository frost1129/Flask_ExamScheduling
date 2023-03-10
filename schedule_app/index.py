import os.path
import csv
import graph_coloring as gc

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
    # Lấy tên file csv
    uploaded_file = os.listdir(app.config['UPLOAD_FOLDER'])
    file_name = None
    for file in uploaded_file:
        file_name = file

    # Sử dụng graph-coloring để phân ngày cho từng môn thi
    sorted_course_day = course_date_sort(file_name)

    # Hiển thị dữ liệu

    return render_template('schedule.html', data=sorted_course_day)


def course_date_sort(file_name):
    # Phân ngày cho các môn thi
    course_dict = {}
    course_graph = gc.Graph()

    # Lấy dữ liệu từ file csv và xử lý thêm vào đồ thị
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            class_code = row['Mã MH']
            student_id = row['MSSV']

            if class_code not in course_dict:
                course_dict[class_code] = []

            course_dict[class_code].append(student_id)

    for c in course_dict:
        course_graph.add_node(c)

    for c1 in course_dict:
        for c2 in course_dict:
            if c1 != c2:
                if set(course_dict[c1]).intersection(set(course_dict[c2])):
                    course_graph.add_edge(c1, c2)

    # Tô màu đồ thị môn học - sinh viên
    colored_graph = gc.welsh_powell(course_graph)
    # Sắp xếp các môn thi theo ngày
    sorted_graph = sorted(colored_graph.items(), key=lambda x: x[1])

    return sorted_graph


@app.route('/delete-csv/<filename>', methods=['POST'])
def delete_csv(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html', message='Xóa file thành công!', cue='success')


if __name__ == '__main__':
    app.run(debug=True)
