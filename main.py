import numpy as np
import pandas as pd
import streamlit as st
import base64 # 載入 model 需要 base64
import pickle

# 用來將字串轉換成整數資料型別的字典
gender = ['Female','Male']                   # 性別:女性是0，男性是1
feature = ['No', 'Yes']                      # 表示是或否的陣列(未/已婚、是/否為自由職業(self-employed))，No為0，Yes為1   
edu = ['Not Graduate', 'Graduate']           # 教育程度:未畢業為0，畢業為1
prop = ['Rural', 'Urban', 'Semiurban']       # 房產地段(Rural:郊區，Urban:都市，Semiurban:近郊區)


## step 1:
## 建立顯示模板

# 取得使用者選擇的顯示頁面(Home跟Prediction)
app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Prediction'])

# 根據使用者選擇切換顯示頁面(Home跟Prediction)
# Home Page:
if app_mode == 'Home':

    st.title('LOAN PREDICTION:')  # 頁面標題
    st.image('hipster_loan-1.jpg')    # 示意圖
    st.markdown('Dataset :')       # markdown 文字方塊
    data = pd.read_csv('loan_dataset.csv') # 取得外部csv資料，來源:https://www.kaggle.com/datasets/burak3ergun/loan-data-set?resource=download
    st.write(data.head())         # 在網頁上顯示前5筆資料
    st.markdown('ApplicantIncome vs LoanAmount :')
    st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20)) # 根據'申請人收入'與'申請貸款金額'的前20筆資料畫出長條圖

# Prediction Page:
elif app_mode == 'Prediction':
    
    # st.image('slider-short-3.jpg')    # 示意圖
    st.image('hipster_loan-1.jpg')    # 示意圖
    # st.subheader('Sir/Mme , You need to fill all necessary informations in order to get a reply to your loan request!') # 子標題
    st.subheader('先生/小姐，請填寫完整資料以申請貸款!') # 子標題
    # 側邊欄
    st.sidebar.header('Informations about the client:') # 側邊欄標題

    # 取得使用者輸入的UI元件
    Gender = st.sidebar.radio('Gender', gender)
    Married = st.sidebar.radio('Married', feature)
    Self_Employed = st.sidebar.radio('Self_Employed', feature)

    Dependents = st.sidebar.radio('Dependents', options=['0', '1', '2', '3+']) # 受撫養的家屬或子女人數
    Education = st.sidebar.radio('Education', edu)                         
    Property_Area = st.sidebar.radio('Property_Area', prop) # 房產地段
    Credit_History = st.sidebar.radio('Credit_History', (0.0, 1.0)) # 信用紀錄評分
    ApplicantIncome = st.sidebar.slider(   # 申請人收入
        label='ApplicantIncome',
        min_value=0,
        max_value=10000,
        value=0,)
    CoapplicantIncome = st.sidebar.slider(   # 共同申請人收入
        label='CoapplicantIncome',
        min_value=0,
        max_value=10000,
        value=0,)
    LoanAmount = st.sidebar.slider('LoanAmount') # 申請貸款額度
    Loan_Amount_Term = st.sidebar.selectbox(      # 抵押貸款期限
        'Loan_Amount_Term',
        (12.0,36.0,60.0,84.0,120.0,180.0,240.0,300.0,360.0))
    
    # 對'受撫養的家屬或子女人數'進行 One-Hot Encoding
    class_0, class_1, class_2, class_3 = 0, 0, 0, 0
    if Dependents == '0':
        class_0 = 1
    elif Dependents == '1':
        class_1 = 1
    elif Dependents == '2':
        class_2 = 1
    else:
        class_3 = 1
    
    # 對'房產地段'進行 One-Hot Encoding
    Rural, Urban, Semiurban = 0, 0, 0
    if Property_Area == 'Rural':
        Rural = 1
    elif Property_Area == 'Urban':
        Urban = 1
    else:
        Semiurban = 1

    # 將取得的使用者輸入進行資料編排
    data1={
    'Gender':Gender,
    'Married':Married,
    'Dependents':[class_0,class_1,class_2,class_3],
    'Education':Education,
    'ApplicantIncome':ApplicantIncome,
    'CoapplicantIncome':CoapplicantIncome,
    'Self Employed':Self_Employed,
    'LoanAmount':LoanAmount,
    'Loan_Amount_Term':Loan_Amount_Term,
    'Credit_History':Credit_History,
    'Property_Area':[Rural,Urban,Semiurban],
    }

    # 整理成要放入model辨識的資料格式
    feature_list=[ApplicantIncome,
                  CoapplicantIncome,
                  LoanAmount,
                  Loan_Amount_Term,
                  Credit_History,
                  gender.index(Gender),
                  feature.index(Married),
                  data1['Dependents'][0],
                  data1['Dependents'][1],
                  data1['Dependents'][2],
                  data1['Dependents'][3],
                  edu.index(Education),
                  feature.index(Self_Employed),
                  data1['Property_Area'][0],
                  data1['Property_Area'][1],
                  data1['Property_Area'][2]]

    single_sample = np.array(feature_list).reshape(1,-1)

    if st.button("Predict"):
        file_ = open("6m-rain.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
   
        file = open("green-cola-no.gif", "rb")
        contents = file.read()
        data_url_no = base64.b64encode(contents).decode("utf-8")
        file.close()
   
        loaded_model = pickle.load(open('Random_Forest.sav', 'rb'))
        prediction = loaded_model.predict(single_sample)
        if prediction[0] == 0 :
            st.error('According to our Calculations, you will not get the loan from Bank')
            st.markdown(f'<img src="data:image/gif;base64,{data_url_no}" alt="cat gif">',unsafe_allow_html=True,)
        elif prediction[0] == 1 :
            st.success('Congratulations!! you will get the loan from Bank')
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',unsafe_allow_html=True,)    