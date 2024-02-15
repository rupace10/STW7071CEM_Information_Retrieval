from django.shortcuts import render
from .forms import SearchForm
from .scraper import crawl_and_scrape, get_index, index_publications, search_index

def index(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = search_index(query)
            return render(request, 'scraperapp/search_results.html', {'results': results})
    return render(request, 'scraperapp/index.html', {'form': form})

def scrape_and_index(request):
    base_url = "https://pureportal.coventry.ac.uk/en/organisations/centre-for-health-and-life-sciences"
    publications = crawl_and_scrape(base_url)
    ix = get_index()
    index_publications(ix, publications)
    return render(request, 'scraperapp/index.html', {'message': 'Scraping and indexing completed successfully.'})
