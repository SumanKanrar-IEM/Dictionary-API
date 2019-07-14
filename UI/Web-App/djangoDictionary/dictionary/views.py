from django.shortcuts import render, HttpResponse
from .dictionaryApp import *

# Create your views here.
# djangoDictionary/dictionary/views.py


def index(request):
    if request.method == 'GET':
        print("GET request received")
        try:
            search_word = request.GET['search_word']
            print("Search_word: ", search_word)
            long_meanings, short_meanings = get_result(search_word)
            print("Long meanings: In GET ", long_meanings)
            print("Short meanings: In GET ", short_meanings)
            if len(short_meanings) == 0:
                dictionary_context = {
                    'long_meanings': long_meanings,
                    'short_meanings': None
                }
            else:
                dictionary_context = {
                    'long_meanings': long_meanings,
                    'short_meanings': short_meanings
                }
            context = {'dictionary': dictionary_context}
            return render(request, 'dictionary/search3.html', context)
            # return HttpResponse(
            #     "<html><head></head><body><p> %s </p></body><html>" %long_meanings
            # )
        except Exception as e:
            print(e)
            return render(request, 'dictionary/search3.html')

