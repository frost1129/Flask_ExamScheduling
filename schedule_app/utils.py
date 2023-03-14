import os
import csv
import graph_coloring as gc

from schedule_app import app


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

    return colored_graph


def temp_time_table(file_name, sorted_course_day):
    course_class = {}
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row['Mã MH']
            name = row['Tên môn']
            classes = row['Lớp']

            if code not in course_class:
                course_class[code] = {'Tên môn': name, 'Lớp': []}

            if classes not in course_class[code]['Lớp']:
                course_class[code]['Lớp'].append(classes)

    exam_list = []

    for exam in sorted_course_day:
        code = exam[0]
        day = exam[1]

        name = course_class[code]['Tên môn']
        classes = course_class[code]['Lớp']
        for cls_name in classes:
            exam_list.append((day, code, name, cls_name))

    return exam_list


def read_course_classes(file_name):
    # Đọc thông tin các lớp của 1 môn học
    classes = {}
    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ma_mh = row['Mã MH']
            lop = row['Lớp']

            if ma_mh not in classes:
                classes[ma_mh] = []

            if not any(cls == lop for cls in classes[ma_mh]):
                classes[ma_mh].append(lop)

    return classes


def create_schedule_dict(course_dict, classes_dict):
    # Tạo dictionary chứa thông tin Ngày thi - (Môn học - Tên lớp)_tuple
    schedule = {}

    for key, value in course_dict.items():
        course = key
        day = value

        classes = classes_dict.get(course, [])
        for c in classes:
            if day not in schedule:
                schedule[day] = []
            schedule[day].append((course, c))

    return schedule


# def welsh_powell_dict(schedule, room_nums):
#     # Sắp xếp các ngày thi theo số lượng lớp thi giảm dần
#     days = sorted(schedule.keys(), key=lambda k: len(schedule[k]), reverse=True)
#
#     # Gán màu giống nhau cho các lớp có cùng môn thi
#     colors = {}
#     for day in days:
#         classes = schedule[day]
#         used_colors = set(colors.get(c, -1) for (c, _) in classes)
#         unused_colors = set(range(room_nums)) - used_colors
#         for (c, _) in classes:
#             if colors.get(c, -1) == -1:
#                 colors[c] = unused_colors.pop()
#
#     # Sắp xếp các lớp thi trong 1 ngày theo thứ tự giảm dần của số lượng lớp thi cùng màu
#     sorted_classes = sorted(colors.keys(), key=lambda k: colors[k])
#
#     # Gán các ca thi cho các lớp
#     slots = {}
#     for c in sorted_classes:
#         color = colors[c]
#         if color not in slots:
#             slots[color] = []
#         day = None
#         for d in days:
#             if (c, _) in schedule[d]:
#                 day = d
#                 break
#         slots[color].append((day, c))
#
#     for color, slot_list in slots.items():
#         sorted_slots = sorted(filter(lambda x: x[0] is not None, slot_list), key=lambda x: x[0])
#         num_slots = len(sorted_slots)
#         slot_size = num_slots // 5 + (1 if num_slots % 5 > 0 else 0)
#         for i, (day, c) in enumerate(sorted_slots):
#             slot_index = i // slot_size
#             if slot_index not in slots[color]:
#                 slots[color][slot_index] = []
#             slots[color][slot_index].append((day, c))
#
#     return slots
#
#
# def print_schedule(schedule_dict):
#     for date, slots in schedule_dict.items():
#         print(f"Date: {date}")
#         for i, slot in enumerate(slots):
#             print(f"Slot {i+1}: {slot}")
#         print()
#
#
# def print_classes(classes_dict):
#     for code, classes in classes_dict.items():
#         print(f'Course code: {code}')
#         for class_info in classes:
#             print(f'- Name: {class_info}')
#

# def print_slots(slots):
#     for color, slot_list in slots.items():
#         print(f'Color {color}:')
#         for i, slot in enumerate(slot_list):
#             print(f'   Slot {i+1}:')
#             print(slot[0])
#             # for day, course in slot:
#             #     print(f'      {day}: {course}')
