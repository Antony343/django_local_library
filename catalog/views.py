from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import Http404, HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

#from .forms import RenewBookForm
from .forms import RenewBookModelForm


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.filter(title__icontains='Gods').count()
    num_genres = Genre.objects.filter(name__icontains='Fantasy').count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # Отрисовка HTML-шаблона base_generic.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_genres': num_genres, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, pk):
        try:
            book_id = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        # book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'catalog/book_detail.html',
            context={'book': book_id, }
        )


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author

    def book_detail_view(request, pk):
        try:
            author_id = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Book does not exist")

        return render(
            request,
            'catalog/author_detail.html',
            context={'author': author_id, }
        )


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/all_borrowed_books_list.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, bookinst_id):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=bookinst_id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'renewal_date': proposed_renewal_date, })
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = ['title', 'author', 'summary', 'isbn']


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')
