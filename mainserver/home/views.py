from datetime import datetime
import pytz
# views.py
import json
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render,redirect
import nltk
import joblib
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from mainserver import settings

# Set-ExecutionPolicy Unrestricted -Scope Process
# .\newsenv\Scripts\activate

# Load the trained model and vectorizer (loaded once globally)
model = joblib.load(settings.BASE_DIR/ 'trained models/fake_news_detector_model.pkl')
vectorizer  = joblib.load(settings.BASE_DIR/ 'trained models/tfidf_vectorizer.pkl')

# Preprocessing function (same as in training)  
def preprocess_text(text):
    import re
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    
    nltk.data.path.append('Server/nltk_data')  # Path to your NLTK data
    
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    words = word_tokenize(text)
    processed_text = [stemmer.stem(word) for word in words if word not in stop_words]

    return ' '.join(processed_text)

def checkFacts(text):
    file =  open("D:\A123\Python 3.6\Python Projects\Fake news Detection\example_response.json","r",encoding="utf8")

    data =  json.load(file)
    data = data['data']
    
    for item in data:
        timestamp_str = item['claim_datetime_utc']
        if timestamp_str is not None:

            datetime_obj = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            item['claim_datetime_utc'] = datetime_obj.replace(tzinfo=pytz.UTC)
        else:
            item['claim_datetime_utc'] = datetime.now()

    return data[:6]


# View to handle predictions
def detect_fake_news(request):

    if request.method == 'POST':
        try:
            news_text = request.POST.get('news_text', '')

            if not news_text:
                    return Response({"error": "News text is required"})


            respon = request.POST.get('check')

            if news_text:
                # Preprocess the news text
                processed_text = preprocess_text(news_text)
                # Vectorize the text
                text_tfidf = vectorizer.transform([processed_text])
                # Predict using the trained model
                prediction = model.predict(text_tfidf)
                # Convert prediction to a human-readable format
                result = "Real News" if prediction[0] == 1 else "Fake News"
                print("the model classes :",model.classes_,prediction)


                input_vector = vectorizer.transform([news_text])
                confidence = model.predict_proba(input_vector)[0]

                # return JsonResponse({'result': result})
                print("Probability :",confidence)

                facts =  checkFacts('')

                return render(request, 'index.html',{
                    "text": news_text,
                    "result": result,
                    "fake":int(round(confidence[0],2)*100),
                    "real":int(round(confidence[1],2)*100),
                    "facts":facts,
                }, status=status.HTTP_200_OK)

                # return render(request, 'index.html',{'result':result,'text':news_text})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        # return JsonResponse({'error': 'No text provided'}, status=400)
        facts =  checkFacts('')
        return render(request, 'index.html',{"facts":facts})
    
def Content(request):
     
  
    return render(request,'about.html')


# views.py

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')  # Redirect to a home page or another view
            else:
                messages.error(request, 'Invalid username or password')
            
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})
