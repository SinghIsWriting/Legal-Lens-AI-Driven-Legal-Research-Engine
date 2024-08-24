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
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request, 'ResearchEngine/landing_page.html')

@login_required
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

@login_required
def upload_document(request):
    if request.method == 'POST':
        try:
            # Get the uploaded file and description
            document = request.FILES.get('document')
            description = request.POST.get('description', '')

            # Handle the file upload logic here (save the file, etc.)
            print(f'FILE is uploaded.\nNAME: {document}\nDESCRIPTION: {description}')

            # Return a JSON response
            return JsonResponse({
                'success':True,
                'message': 'Document uploaded successfully!',
                'document_name': document.name,
            })
        except Exception as e:
            return JsonResponse({
                'success':False,
                'error': str(e)
            })
    # if request.method == 'POST':
    #     document = request.FILES['document']
    #     # Process the uploaded document
    #     title, content, court, case_number, date = process_document(document)
    #     legal_doc = LegalDocument.objects.create(
    #         title=title, content=content, court=court,
    #         case_number=case_number, date=date
    #     )

    #     # Use the Research Engine to extract information and predict the outcome
    #     research_engine = ResearchEngine()
    #     research_engine.aggregate_and_process_data()
    #     key_principles, precedents = research_engine.extract_information(content)
    #     predicted_outcome = research_engine.predict_case_outcome(content)

    #     # Save the case outcome prediction
    #     CaseOutcome.objects.create(
    #         case=legal_doc, predicted_outcome=predicted_outcome,
    #         actual_outcome="To be updated"
    #     )

    #     return redirect('search')
    elif request.method == 'GET':
        return render(request, 'ResearchEngine/upload.html')

@login_required
def prediction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            case_summary = data.get('case_summary')
            case_type = data.get('case_type')
            jurisdiction = data.get('jurisdiction')

            # Process the data and perform prediction
            predicted_outcome = '''<p>The court is likely to rule in favor of the plaintiff, granting monetary compensation for the damages incurred.<br>
                <strong>Reasoning:</strong> Based on the case summary and relevant legal precedents, the plaintiff has established a clear basis for their claim, supported by strong evidence.<br>
                <strong>Case Type:</strong> Civil<br>
                <strong>Jurisdiction:</strong> High Court<br>
                <strong>Confidence Level:</strong> <span style="color: green;">85%</span>
            </p>
            <p>
                <em>Note:</em> The prediction is based on the available information and historical data. Actual outcomes may vary.
            </p>'''

            # Return the result as JSON
            return JsonResponse({
                'success': True,
                'predicted_outcome': mark_safe(predicted_outcome)
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    # if request.method == 'POST':
    #     query = request.POST['query']
    #     # Perform search and retrieve relevant documents
    #     documents = LegalDocument.objects.filter(
    #         content__icontains=query
    #     )
    #     return render(request, 'ResearchEngine/prediction.html', {'documents': documents})
    return render(request, 'ResearchEngine/prediction.html')

@login_required
def query_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        case_type = data.get('case_type')
        resultCount = data.get('resultCount')

        # Process the query and case_type (you can add your own logic here)
        response_text = f"Received your {case_type} search query: {query}, Result shown count: {resultCount}"

        # Example JSON response
        return JsonResponse({'response': response_text})
    return render(request, 'ResearchEngine/query_page.html')


