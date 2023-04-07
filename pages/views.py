from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def homePageView(request):
    return render(request, 'home.html')

def dataView(request):
    # return request object and specify page.
    return render(request, 'data.html')


def homePost(request):
    # Use request object to extract choice.

    age = 0
    active = None
    gender = None
    bank_balance = 0
    num_products = 0

    try:
        # Extract value from request object by control name. 
        age = int(request.POST['age'])
        active = request.POST['active_member']
        gender = request.POST['gender']
        bank_balance = int(request.POST['bank_balance'])
        num_products = int(request.POST['num_products'])
        
        # # Crude debugging effort. 
        # print("*** Years work experience: " + str(currentChoice))
        # choice    = int(currentChoice)
        # gmat = float(gmatStr)
    # Enters 'except' block if integer cannot be created.
    except Exception as e:
        print(e)
        return render(request, 'home.html', {
            'errorMessage': f'*** An error occurred: {str(e)}. Please try again.'
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={
            'age': age,
            'active_member': active,
            'gender': gender,
            'bank_balance': bank_balance,
            'num_products': num_products,
        },))
        

import pickle
import sklearn # You must perform a pip install.
import pandas as pd

def results(request, age, active_member, gender, bank_balance, num_products):
    print("*** Inside reults()")
    active_string = active_member
    active_member = 1 if active_member == 'Yes' else 0
    if gender == 'male':
        Gender_Male = 1
        Gender_Female = 0
    else:
        Gender_Male = 0
        Gender_Female = 1


    # load saved model
    with open('./model.pkl' , 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDf = pd.DataFrame(columns=['Age', 'IsActiveMember', 'Gender_Male','Gender_Female',
                                           'Balance','NumOfProducts'])

    # print("*** GMAT Score: " + str(gmat))
    # print("*** Years experience: " + str(workExperience))
    singleSampleDf = singleSampleDf.append({
        'Age': age,
        'IsActiveMember':active_member,
        'Gender_Male': Gender_Male,
        'Gender_Female': Gender_Female,
        'Balance': bank_balance,
        'NumOfProducts': num_products,        
    },ignore_index=True)

    # load scaler
    with open('./scaler.pkl' , 'rb') as f:
        sc = pickle.load(f)
    
    sc.transform(singleSampleDf)
    
    singlePrediction = loadedModel.predict(singleSampleDf)

    print(singlePrediction)
    print(type(singlePrediction))

    singlePrediction = singlePrediction[0]

    print("Single prediction: " + str(singlePrediction))


    return render(request, 'results.html', {
        'age': age,
        'active_member': active_string,
        'gender': gender,
        'bank_balance': bank_balance,
        'num_products': num_products,
        'singlePrediction': singlePrediction,
    })
