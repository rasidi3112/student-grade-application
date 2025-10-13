


# cuplikan kode Python Flask
#Import Library:
#Pertama, import semua library yang dibutuhkan:

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import json
import os
import pandas as pd
from datetime import datetime
import pdfkit
from io import BytesIO
import tempfile



#Inisialisasi Flask:
#Bikin objek Flask seperti biasa.
app = Flask(__name__)

# kode lengkap menangani route '/', '/add', '/grades', '/laporan', '/export/pdf', '/export/excel'
# dan JSON API ada di dokumentasi dan project utama.


#Database Sederhana dengan JSON:
#Karena kita gak pakai SQL, jadi data mahasiswa disimpan di file students.json.
#Ada dua fungsi utama: 
DB_FILE = 'students.json'
#Fungsi get_students() untuk ambil data, dan save_students() untuk simpan data.




#Fungsi Mengubah Nilai Angka ke Grade Huruf:
#Supaya ada grade A, B, C, D, E:
def get_students():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []



def save_students(students):
    with open(DB_FILE, 'w') as f:
        json.dump(students, f, indent=4)




def get_grade_letter(grade):
    if grade >= 85:
        return 'A'
    elif grade >= 75:
        return 'B'
    elif grade >= 65:
        return 'C'
    elif grade >= 55:
        return 'D'
    else:
        return 'E'

def calculate_stats(students):
    if not students:
        return {
            'average': 0,
            'highest': 0,
            'lowest': 0,
            'count': 0,
            'passing': 0,
            'failing': 0
        }
    
    grades = [s['grade'] for s in students]
    passing_count = sum(1 for g in grades if g >= 55)
    
    return {
        'average': sum(grades) / len(grades),
        'highest': max(grades),
        'lowest': min(grades),
        'count': len(students),
        'passing': passing_count,
        'failing': len(grades) - passing_count
    }

def get_top_students(students, count=3):
    if not students:
        return []
    
    sorted_students = sorted(students, key=lambda x: x['grade'], reverse=True)
    return sorted_students[:count]

def calculate_semester_stats(students):
    semester_stats = {}
    
    for student in students:
        semester = student['semester']
        grade = student['grade']
        
        if semester not in semester_stats:
            semester_stats[semester] = {
                'total': 0,
                'count': 0,
                'grades': []
            }
        
        semester_stats[semester]['total'] += grade
        semester_stats[semester]['count'] += 1
        semester_stats[semester]['grades'].append(grade)
    
    # Calculate average for each semester
    for semester in semester_stats:
        semester_stats[semester]['average'] = (
            semester_stats[semester]['total'] / semester_stats[semester]['count']
        )
    
    return semester_stats

def calculate_course_stats(students):
    course_stats = {}
    
    for student in students:
        course = student['course']
        grade = student['grade']
        
        if course not in course_stats:
            course_stats[course] = {
                'total': 0,
                'count': 0,
                'grades': []
            }
        
        course_stats[course]['total'] += grade
        course_stats[course]['count'] += 1
        course_stats[course]['grades'].append(grade)
    
    # Calculate average for each course
    for course in course_stats:
        course_stats[course]['average'] = (
            course_stats[course]['total'] / course_stats[course]['count']
        )
    
    return course_stats

def calculate_grade_distribution(students):
    grade_distribution = {
        'A': 0,
        'B': 0,
        'C': 0,
        'D': 0,
        'E': 0
    }
    
    for student in students:
        grade = get_grade_letter(student['grade'])
        grade_distribution[grade] += 1
    
    return grade_distribution





#Routing Utama: HOME
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        students = get_students()
        
        student_id = f"STD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        new_student = {
            'id': student_id,
            'name': request.form['name'],
            'npm': request.form['npm'],
            'course': request.form['course'],
            'grade': float(request.form['grade']),
            'semester': request.form['semester'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        students.append(new_student)
        save_students(students)
        
        return redirect(url_for('view_grades'))
    
    return render_template('add_student.html')

@app.route('/grades')
def view_grades():
    students = get_students()
    return render_template('view_grades.html', students=students)

@app.route('/laporan')
def report():
    students = get_students()
    stats = calculate_stats(students)
    top_students = get_top_students(students, 3)
    semester_stats = calculate_semester_stats(students)
    course_stats = calculate_course_stats(students)
    grade_distribution = calculate_grade_distribution(students)
    
    return render_template(
        'report.html',
        students=students,
        stats=stats,
        top_students=top_students,
        semester_stats=semester_stats,
        course_stats=course_stats,
        grade_distribution=grade_distribution,
        date_now=datetime.now().strftime('%d %B %Y %H:%M'),
        total_students=len(students)
    )

@app.route('/export/pdf')
def export_pdf():
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    options = {'enable-local-file-access': ''}
    students = get_students()
    stats = calculate_stats(students)
    top_students = get_top_students(students)
    semester_stats = calculate_semester_stats(students)
    course_stats = calculate_course_stats(students)
    grade_distribution = calculate_grade_distribution(students)
    html_content = render_template('report.html', students=students, stats=stats, top_students=top_students,
                                   semester_stats=semester_stats, course_stats=course_stats,
                                   grade_distribution=grade_distribution,
                                   date_now=datetime.now().strftime('%d %B %Y %H:%M'), total_students=len(students))
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
        temp_html.write(html_content.encode('utf-8'))
        temp_html_path = temp_html.name
    output_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    pdfkit.from_file(temp_html_path, output_pdf.name, configuration=config, options=options)
    os.unlink(temp_html_path)
    return_data = BytesIO()
    with open(output_pdf.name, 'rb') as f:
        return_data.write(f.read())
    os.unlink(output_pdf.name)
    return_data.seek(0)
    filename = f"Laporan_Nilai_Mahasiswa_{datetime.now().strftime('%Y%m%d')}.pdf"
    return send_file(return_data, mimetype='application/pdf', as_attachment=True, download_name=filename)


@app.route('/export/excel')
def export_excel():
    students = get_students()
    
    # Create DataFrame from students data
    df = pd.DataFrame(students)
    
    # Add grade letter column
    df['grade_letter'] = df['grade'].apply(get_grade_letter)
    
    # Select and rename columns for the Excel file
    excel_df = df[['name', 'npm', 'course', 'grade', 'grade_letter', 'semester', 'timestamp']]
    excel_df.columns = ['Nama', 'NPM', 'Mata Kuliah', 'Nilai', 'Grade', 'Semester', 'Tanggal Input']
    
    # Create Excel writer
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write students data to the first sheet
        excel_df.to_excel(writer, sheet_name='Data Nilai', index=False)
        
        # Create summary sheet
        stats = calculate_stats(students)
        semester_stats = calculate_semester_stats(students)
        course_stats = calculate_course_stats(students)
        grade_distribution = calculate_grade_distribution(students)
        
        # Create and write summary data
        summary_data = {
            'Metrik': [
                'Rata-rata Nilai', 
                'Nilai Tertinggi', 
                'Nilai Terendah',
                'Total Mahasiswa',
                'Mahasiswa Lulus',
                'Mahasiswa Tidak Lulus'
            ],
            'Nilai': [
                round(stats['average'], 2),
                stats['highest'],
                stats['lowest'],
                stats['count'],
                stats['passing'],
                stats['failing']
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Ringkasan', index=False, startrow=1)
        
        # Create sheet for semester stats
        semester_data = []
        for semester, data in semester_stats.items():
            semester_data.append({
                'Semester': semester,
                'Rata-rata': round(data['average'], 2),
                'Jumlah Mahasiswa': data['count']
            })
        
        if semester_data:
            semester_df = pd.DataFrame(semester_data)
            semester_df.to_excel(writer, sheet_name='Per Semester', index=False)
        
        # Create sheet for course stats
        course_data = []
        for course, data in course_stats.items():
            course_data.append({
                'Mata Kuliah': course,
                'Rata-rata': round(data['average'], 2),
                'Jumlah Mahasiswa': data['count']
            })
        
        if course_data:
            course_df = pd.DataFrame(course_data)
            course_df.to_excel(writer, sheet_name='Per Mata Kuliah', index=False)
    
    output.seek(0)
    
    # Set filename with current date
    filename = f"Laporan_Nilai_Mahasiswa_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/students', methods=['GET'])
def api_students():
    students = get_students()
    return jsonify(students)

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    students = get_students()
    students = [s for s in students if s['id'] != student_id]
    save_students(students)
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def stats():
    students = get_students()
    stats = calculate_stats(students)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
    