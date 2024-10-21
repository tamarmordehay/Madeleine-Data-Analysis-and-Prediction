
import pandas as pd
import numpy as np
from madlan_data_prep import prepare_data
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from numpy import sqrt
from numpy import mean
from numpy import absolute
import pickle
from sklearn.model_selection import train_test_split

df = pd.read_excel("output_all_students_Train_v10.xlsx")

data = prepare_data(df)

def missing_values_and_feature_engineering_and_catgorial_data(data):
    #טיפול בדאטה קטגורי
    City_dum=pd.get_dummies(data['City'])
#    type_dum=pd.get_dummies(data['type'])
#    city_area_dum = pd.get_dummies(data['city_area'])
#    condition_dum = pd.get_dummies(data['condition '])
    
#טיפול בערכים חסרים
    old_string = 'NaN' 
    new_string = ''
    data['Area'] = data['Area'].replace(old_string, new_string)

#יצירת עמודה חדשה ששומרת את אחוז מיקום הקומה בבניין
#בסוף לא השתמשנו בעמודה זו כי המודל לא עובד עם משתנה FLOAT
    # data['floor'] = pd.to_numeric(data['floor'], errors='coerce')
    # data['total_floors'] = pd.to_numeric(data['total_floors'], errors='coerce')
    # data['floor_out_of_floors'] = data['floor'] / data['total_floors'] 

#המרת דאטה SRT לדאטה מספרי
    data['Area'] = pd.to_numeric(data['Area'], errors='coerce')

    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    
    #בחירת עמודות רלוונטיות
    model_data = data[['Area','hasElevator ','hasParking ', 'hasBars ', 'hasStorage ','hasAirCondition ','hasBalcony ', 'hasMamad ', 'handicapFriendly ','price']]
    
#יצירת DF אחוד
    model_data = pd.merge( City_dum, model_data, left_index=True, right_index=True)
#    model_data = pd.merge( type_dum, model_data, left_index=True, right_index=True)
#    model_data = pd.merge( city_area_dum, model_data, left_index=True, right_index=True)
#   model_data = pd.merge( condition_dum, model_data, left_index=True, right_index=True)
    model_data = model_data.dropna()
    
    return(model_data)

#ברגע שפיצלנו את הדאטה לפני השמת הפונקציה קיבלנו שגיאה שלא הצלחנו להתגבר עליה
#הפונקציה מבצעת את כל הפעולות שצינור היה אמור לבצע
model_data = missing_values_and_feature_engineering_and_catgorial_data(data)
x=model_data.iloc[ : , 0:38].values
y=model_data.iloc[ : ,38].values
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 0)#פיצול של 40 60 מביא שגיאות מפוזרות גם לצד החיובי וגם לשלילי

#---------------------------------------------------------------------------------------------------------------------
#רגרסיה פולינומיאלית 


# degrees = [1,2] #מעבר לדרגה 2 לא ניתן להריץ בגלל מגבלת הזיכרון במחשב
# train_errors = []

# for degree in degrees:
#     poly_features = PolynomialFeatures(degree=degree, include_bias=False)
#     X_train_poly = poly_features.fit_transform(x)
#     lin_reg = LinearRegression()
#     lin_reg.fit(X_train_poly, y)
#     y_train_predict = lin_reg.predict(X_train_poly)
#     train_errors.append(mean_squared_error(y, y_train_predict))
# plt.plot(degrees, np.sqrt(train_errors),"r-+", linewidth=2, label="train")
# plt.legend(loc="upper right", fontsize=14)
# plt.xlabel("Degree", fontsize=14)
# plt.ylabel("RMSE", fontsize=14)
# plt.show()

# print(min(train_errors))


#---------------------------------------------------------------------------------------------------------------------
#רגרסיה מורכבת
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
error = y_test-y_pred
plt.hist(error)
#print(regressor.coef_)

print(mean_squared_error(y_test, y_pred))

#---------------------------------------------------------------------------------------------------------------------
#בדיקת נכונות המודל

cv = KFold(n_splits=15, random_state=1, shuffle=True) 

scores = cross_val_score(regressor, x, y, scoring='neg_mean_squared_error',cv=cv, n_jobs=-1)

sqrt(mean(absolute(scores)))

#plt.hist(scores)

#הרצנו את המודל בצורה רנדומאלית עם אותה החלוקה של אימון ומבחן 15 פעמים
#מתוך 15 פעמים רואים שהשגיאה נמצאת בטווח זהה מלבד מקרה בודד לכן נניח שהמודל תקין


cv = KFold(n_splits=40, random_state=1, shuffle=True) 

scores = cross_val_score(regressor, x, y, scoring='neg_mean_squared_error',cv=cv, n_jobs=-1)

sqrt(mean(absolute(scores)))

#plt.hist(scores)

#כאשר מגדילים את כמות הפיצולים ניתן לראות שאותה חריגה חוזרת 
#לכן ניתן להניח שהמודל תקין ב 9/10 פעמים

#---------------------------------------------------------------------------------------------------------------------
pickle.dump(regressor, open("trained_model.pkl","wb"))
