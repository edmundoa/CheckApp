from django.shortcuts import render_to_response

def view_404(request):
    return render_to_response('custom_404.html')

def view_500(request):
    return render_to_response('custom_500.html')


