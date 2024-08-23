from django.shortcuts import render, redirect
from .models import LegalDocument, CaseOutcome
# from .utils import process_document, predict_outcome

# def home(request):
#     return render(request, 'researchEngine/home.html')

# def upload_document(request):
#     if request.method == 'POST':
#         document = request.FILES['document']
#         # Process the uploaded document
#         title, content, court, case_number, date = process_document(document)
#         legal_doc = LegalDocument.objects.create(
#             title=title, content=content, court=court,
#             case_number=case_number, date=date
#         )
#         # Predict the outcome of the case
#         predicted_outcome, actual_outcome = predict_outcome(content)
#         CaseOutcome.objects.create(
#             case=legal_doc, predicted_outcome=predicted_outcome,
#             actual_outcome=actual_outcome
#         )
#         return redirect('search')
#     return render(request, 'researchEngine/upload.html')

# def search(request):
#     if request.method == 'POST':
#         query = request.POST['query']
#         # Perform search and retrieve relevant documents
#         documents = LegalDocument.objects.filter(
#             content__icontains=query
#         )
#         return render(request, 'ResearchEngine/search.html', {'documents': documents})
#     return render(request, 'researchEngine/search.html')


from django.shortcuts import render, redirect
from .models import LegalDocument, CaseOutcome
from .utils import ResearchEngine
import json
from django.http import JsonResponse, HttpResponse

def landing_page(request):
    return render(request, 'ResearchEngine/landing_page.html')

def home(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', '')

        # Process the query and generate a response (replace this with your actual logic)
        bot_response = f'''You asked: {query}. Here's a response from the AI.'''
        return JsonResponse({'response': bot_response})
    return render(request, 'ResearchEngine/home.html')

def about(request):
    return render(request, 'ResearchEngine/about.html')

def contact(request):
    return render(request, 'ResearchEngine/contact.html')

def upload_document(request):
    if request.method == 'POST':
        document = request.FILES['document']
        # Process the uploaded document
        title, content, court, case_number, date = process_document(document)
        legal_doc = LegalDocument.objects.create(
            title=title, content=content, court=court,
            case_number=case_number, date=date
        )

        # Use the Research Engine to extract information and predict the outcome
        research_engine = ResearchEngine()
        research_engine.aggregate_and_process_data()
        key_principles, precedents = research_engine.extract_information(content)
        predicted_outcome = research_engine.predict_case_outcome(content)

        # Save the case outcome prediction
        CaseOutcome.objects.create(
            case=legal_doc, predicted_outcome=predicted_outcome,
            actual_outcome="To be updated"
        )

        return redirect('search')
    return render(request, 'ResearchEngine/upload.html')

def prediction(request):
    if request.method == 'POST':
        query = request.POST['query']
        # Perform search and retrieve relevant documents
        documents = LegalDocument.objects.filter(
            content__icontains=query
        )
        return render(request, 'ResearchEngine/prediction.html', {'documents': documents})
    return render(request, 'ResearchEngine/prediction.html')

def query(request):
    if request.method == 'POST':
        query = request.POST['query']
        # Perform search and retrieve relevant documents
        documents = []
        return render(request, 'ResearchEngine/query_page.html', {'documents': documents})
    return render(request, 'ResearchEngine/query_page.html')


