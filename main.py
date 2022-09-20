# Import Libraries.
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np


# Loading Transformer & Model.
transformer = joblib.load("transformer.pkl")
model = joblib.load("model.pkl")

# App Initialization.
app = FastAPI(title="MLOps API")
templates = Jinja2Templates(directory="templates/")

# Paths.
# For normal testing.
@app.get('/')
def read_form():
    return 'Hello World From FastAPI!!     **If you want to go to the main app page append /form in the url bar.**'

# For getting Inputs from User.
@app.get("/form")
def form_post(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

# For Prediction & Returning the Output to User.
@app.post("/form")
def form_post(  request         : Request        , 
                creditscore     : int = Form(...), 
                geography       : str = Form(...),  
                gender          : str = Form(...), 
                age             : int = Form(...), 
                balance         : int = Form(...), 
                numofproducts   : int = Form(...), 
                isactivemember  : int = Form(...)
            ):

    output_dict = {"CreditScore": creditscore, "Geography": geography, "Gender": gender, "Age": age, "Balance(in $)": balance, "Num Of Products": numofproducts, "Is Active Member": isactivemember }
    input_data_org = [
                    [
                       creditscore,
                       geography,
                       gender,
                       age,
                       balance,
                       numofproducts,
                       isactivemember 
                    ]
                ]    
    input_data = transformer.transform(input_data_org)

    # output_text_dict = {0: "Customer will not going to Exit in future!!",
    #                1: "Customer will going to Exit in future!!"
    #                }

    fun_output_text_dict = {0: "'\N{Face With Party Horn And Party Hat}' कहीं नहीं जाएगा ये ग्राहक!!' \N{Face With Party Horn And Party Hat}'" ,
                       1: "'\N{loudly crying face}' जाने वाले को कौन रोक सकाता है!!' \N{loudly crying face}'"}

    output_dict['Prediction Probability'] = model.predict_proba(input_data).tolist()[0]
    output_dict['Prediction Probability'] = np.round_(output_dict['Prediction Probability'], decimals=2)
    output_dict['Prediction'] = model.predict(input_data).tolist()[0]
    
    #output_dict['Significance'] = output_text_dict[ output_dict['Prediction'] ]

    output_dict['Significance'] = fun_output_text_dict[ output_dict['Prediction'] ]

    print(output_dict)
    print(type(output_dict))

    return templates.TemplateResponse('output.html', context={'request': request, 'output': output_dict})
