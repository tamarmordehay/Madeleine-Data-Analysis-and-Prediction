import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta


df = pd.read_excel("output_all_students_Train_v10.xlsx")

def prepare_data(df):
    
    test = df
    
    #מחיקת כל השורות ללא מחיר
    
    test = test.dropna(subset=['price'], inplace=False)
    
    #המרת מחיר ליחידות מספריות
    test['price'] = test['price'].apply(lambda x: re.sub('[^\d.]', '', str(x)))
    
    
    #המרת שטח ליחידות מספריות
    test = test.dropna(subset=['Area'], inplace=False) #יש 3 שורות שנשארות ריקות למרות הפונקציה
    test['Area'] = test['Area'].apply(lambda x: re.sub('[^\d.]', '', str(x)))
    
    
    #הורדת סימני פיסוק לעמודות שונות
    test['Street'] = df['Street'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)).replace('\d+', ''))
    
    test['city_area'] = df['city_area'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)).replace('\d+', ''))
    
    test['description '] = df['description '].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)).replace('\d+', ''))
    
    test['hasMamad '] = df['hasMamad '].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)).replace('\d+', ''))
    
    
    #יצירת עמודה קומה וטיפול בערכים ייחודיים
    old_string = 'קומת קרקע'
    new_string = 'קומה 0'
    test['floor_out_of'] = test['floor_out_of'].replace(old_string, new_string)
    
    
    old_string = 'קומת מרתף'
    new_string = 'קומה -1'
    test['floor_out_of'] = test['floor_out_of'].replace(old_string, new_string)
    
    
    target_word = 'קומה'
    test['floor'] = test['floor_out_of'].str.extract(rf'{target_word}\s*(\d+)', flags=re.IGNORECASE)
    
    
    #יצירת עמודה כל הקומות בבנין
    target_word = 'מתוך'
    test['total_floors'] = test['floor_out_of'].str.extract(rf'{target_word}\s*(\d+)', flags=re.IGNORECASE)
    
    
    # יצירת עמודת תאריך גניסה קטגורית
    today = datetime.today().date()
    six_months_from_now = today + timedelta(6*30)
    
    old_string = 'גמיש'
    new_string = 'flexible'
    test['entrance_date'] = test['entranceDate '].replace(old_string, new_string)
    
    old_string = 'גמיש '
    new_string = 'flexible'
    test['entrance_date'] = test['entrance_date'].replace(old_string, new_string)
    
    old_string = 'לא צויין'
    new_string = 'not_defined'
    test['entrance_date'] = test['entrance_date'].replace(old_string, new_string)
    
    old_string = "מיידי"
    new_string = 'less_than_6 months '
    test['entrance_date'] = test['entrance_date'].replace(old_string, new_string)
    
    test['entrance_date'] = test['entrance_date'].apply(lambda x: 'More_than_6 months' if isinstance(x, datetime) and x.date() > today + timedelta(days=365/2) and x.date() <= today + timedelta(days=365) 
                                                else 'less_than_6 months' if isinstance(x, datetime) and x.date() <= today + timedelta(days=365/2)
                                                else 'Above_year' if isinstance(x, datetime) and x.date() > today + timedelta(days=366)
                                                else x)
    
    
    
    # יש מעלית
    old_string = 'כן'
    new_string = True
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'יש מעלית'
    new_string = True
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'אין מעלית'
    new_string = False
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasElevator '] = test['hasElevator '].replace(old_string, new_string)
    
    test = test.dropna(subset=['hasElevator '], inplace=False)
    
    test['hasElevator '] = test['hasElevator '].astype(int)
     
    
    #יש חניה
    old_string = 'כן'
    new_string = True
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'יש חניה'
    new_string = True
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'יש חנייה'
    new_string = True
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'אין חניה'
    new_string = False
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasParking '] = test['hasParking '].replace(old_string, new_string)
    
    test = test.dropna(subset=['hasParking '], inplace=False)
    
    test['hasParking '] = test['hasParking '].astype(int)
    
    
    #יש סורגים
    old_string = 'כן'
    new_string = True
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'יש סורגים'
    new_string = True
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'אין סורגים'
    new_string = False
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasBars '] = test['hasBars '].replace(old_string, new_string)
    
    test = test.dropna(subset=['hasBars '], inplace=False)
    
    test['hasBars '] = test['hasBars '].astype(int)
    
    
    # יש מחסן
    old_string = 'כן'
    new_string = True
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'יש מחסן'
    new_string = True
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'אין מחסן'
    new_string = False
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasStorage '] = test['hasStorage '].replace(old_string, new_string)
    
    test = test.dropna(subset=['hasStorage '], inplace=False)
    
    test['hasStorage '] = test['hasStorage '].astype(int)
    
    
    
    # יש מיזוג אויר
    old_string = 'כן'
    new_string = True
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'יש מיזוג אויר'
    new_string = True
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'יש מיזוג אוויר'
    new_string = True
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'אין מיזוג אויר'
    new_string = False
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasAirCondition '] = test['hasAirCondition '].replace(old_string, new_string)
    
    test = test.dropna(subset=['hasAirCondition '], inplace=False)
    
    test['hasAirCondition '] = test['hasAirCondition '].astype(int)
    
    
    
    #יש מרפסת
    old_string = 'כן'
    new_string = True
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'יש מרפסת'
    new_string = True
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'אין מרפסת'
    new_string = False
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasBalcony '] = test['hasBalcony '].replace(old_string, new_string)
    
    test = test.dropna(subset=['hasBalcony '], inplace=False)
    
    test['hasBalcony '] = test['hasBalcony '].astype(int)
    
    
    
    
    #יש ממד
    old_string = 'כן'
    new_string = True
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'יש ממד'
    new_string = True
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'אין ממד'
    new_string = False
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'יש'
    new_string = True
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'אין'
    new_string = False
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'True'
    new_string = True
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    old_string = 'False'
    new_string = False
    test['hasMamad '] = test['hasMamad '].replace(old_string, new_string)
    test = test.dropna(subset=['hasMamad '], inplace=False)
    
    test['hasMamad '] = test['hasMamad '].astype(int)
    
    
    #יש נגישות להכים
    old_string = 'כן'
    new_string = True
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'לא'
    new_string = False
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'yes'
    new_string = True
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'no'
    new_string = False
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'נגיש'
    new_string = True
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'לא נגיש'
    new_string = False
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'נגיש לנכים'
    new_string = True
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    old_string = 'לא נגיש לנכים'
    new_string = False
    test['handicapFriendly '] = test['handicapFriendly '].replace(old_string, new_string)
    
    test = test.dropna(subset=['handicapFriendly '], inplace=False)
    
    test['handicapFriendly '] = test['handicapFriendly '].astype(int)
    
#טיפול בערכים שונים בעמודת עיר
    old_string = 'נהרייה' 
    new_string = 'נהריה'
    test['City'] = test['City'].replace(old_string, new_string)
    
    old_string = ' נהריה' 
    new_string = 'נהריה'
    test['City'] = test['City'].replace(old_string, new_string)
    
    old_string = ' שוהם' 
    new_string = 'שוהם'
    test['City'] = test['City'].replace(old_string, new_string)    
    
    column_to_move="price"
    column = test.pop(column_to_move)
    test.insert(25, column.name, column)
    
    return test

    
    
    
    
    
    
