from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from book.models import Book
from author.models import Author
from django.views.generic import DetailView


@login_required
def books_page(request):
    book = Book.objects.all()
    if request.method == 'POST':
        if request.POST['parameter'] is None or not request.POST['value']:
            book = Book.objects.all()
        elif request.POST['parameter'] == "authors":
            book = Book.objects.filter(authors__surname__icontains=request.POST['value']).values()
        elif request.POST['parameter'] == "title":
            book = Book.objects.filter(name__icontains=request.POST['value']).values()
        return render(request, template_name='book/book.html',
                      context={'books': book, 'parameter': request.POST['parameter'], 'value': request.POST['value']})
    else:
        return render(request, template_name='book/book.html',
                      context={'books': book})


@method_decorator(login_required, name='dispatch')
class BookDetails(DetailView):
    model = Book
    template_name = 'book/book_details.html'


@login_required
def add_book_view(request):
    if request.method == 'GET':
        return render(request, template_name='book/add_book.html',
                      context={'authors': Author.get_all().order_by('surname')})
    else:
        authors_id = request.POST.getlist('authors')
        name = request.POST['name']
        description = request.POST['description']
        count = request.POST['count']
        try:
            list_authors = [Author.get_by_id(int(id)) for id in authors_id]
            book_to_add = Book.create(name=name, description=description, count=count,
                                      authors=list_authors)
            book_to_add.save()
        except Exception as error:
            return HttpResponse(error)

        book = Book.objects.all()
        return render(request, template_name='book/book.html',
                      context={'books': book})


@login_required
def remove_book(request, book_id):
    if request.method == 'POST':
        book_to_remove = Book.get_by_id(book_id)
        book_to_remove.delete()
        return redirect('book:book')
