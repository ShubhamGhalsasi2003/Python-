import pandas as pd
import re

def find_absent_streaks(attendance_df):
 
    attendance_df = attendance_df.sort_values(by=['student_id', 'attendance_date'])

    absence_streaks = []
    
    for student_id, group in attendance_df.groupby('student_id'):
        group = group.reset_index(drop=True)
        absences = group[group['status'] == 'Absent']
        
        if not absences.empty:
            start_date, end_date = None, None
            count = 0
            
            for i in range(len(absences)):
                if i == 0 or (pd.to_datetime(absences.iloc[i]['attendance_date']) - pd.to_datetime(absences.iloc[i - 1]['attendance_date'])).days == 1:
                    count += 1
                    if start_date is None:
                        start_date = absences.iloc[i]['attendance_date']
                    end_date = absences.iloc[i]['attendance_date']
                else:
                    if count > 3:
                        absence_streaks.append([student_id, start_date, end_date, count])
                    start_date, end_date = absences.iloc[i]['attendance_date'], absences.iloc[i]['attendance_date']
                    count = 1
            
            if count > 3:
                absence_streaks.append([student_id, start_date, end_date, count])
    
    absence_df = pd.DataFrame(absence_streaks, columns=['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days'])
    return absence_df

def validate_email(email):
    email_pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*@[a-zA-Z]+\.(com)$'
    return bool(re.match(email_pattern, email))

def run():
    attendance_data = {
        'student_id': [1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
        'attendance_date': ['2025-03-20', '2025-03-21', '2025-03-22', '2025-03-23',  '2025-03-18', '2025-03-19', '2025-03-20', '2025-03-21', '2025-03-22',  '2025-03-15', '2025-03-16', '2025-03-17', '2025-03-18', '2025-03-19'],
        'status': ['Absent', 'Absent', 'Absent', 'Absent',  'Present', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Present']
    }
    attendance_df = pd.DataFrame(attendance_data)
    
    absence_df = find_absent_streaks(attendance_df)
    
    students_data = {
        'student_id': [1, 2, 3],
        'student_name': ['Alice', 'Bob', 'Charlie'],
        'parent_email': ['alice_parent@gmail.com', 'bob_parent@edu', 'charlie123@yahoo.com']
    }
    students_df = pd.DataFrame(students_data)
    
    final_df = absence_df.merge(students_df, on='student_id', how='left')
    
    final_df['email'] = final_df['parent_email'].apply(lambda x: x if validate_email(x) else None)
    final_df['msg'] = final_df.apply(lambda row: f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date']} to {row['absence_end_date']} for {row['total_absent_days']} days. Please ensure their attendance improves."
     if row['email'] is not None else None, axis=1)
    
    final_df = final_df[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]
    
    return final_df

result_df = run()
print(result_df)
