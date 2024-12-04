from django.shortcuts import render, redirect
import pandas as pd
from .models import Stock
from django.views.decorators.cache import cache_page


# Create your views here.
@cache_page(60 * 15)
def home(request):
    if Stock.objects.exists():
        latest_file = Stock.objects.last().file.path
        try:
            df = pd.read_csv(latest_file)
            data_html = df.to_html(classes="table table-striped")
        except Exception as e:
            data_html = f"<p>Error reading file: {str(e)}</p>"
    else:
        data_html = "<p>No data uploaded</p>"
    return render(request, 'home.html', {'data_html': data_html})


def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES['csv_file']
        Stock.objects.create(file=file)
        return redirect('home')
    return render(request, 'upload.html')


def data_visualization(request):
    return render(request, 'data_visualization.html')


def data_analysis(request):
    return render(request, 'data_analysis.html')
