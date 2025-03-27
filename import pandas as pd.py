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
       
