from django.shortcuts import render

# Create your views here.


def minesweeper(request):
    return render(request, "minesweeper/mine.html")
