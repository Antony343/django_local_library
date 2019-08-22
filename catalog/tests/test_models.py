from django.test import TestCase

# Create your tests here.

from catalog.models import Author, Book, Genre


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Book.objects.create(title='Snowflake', isbn='9781547065769')
        Genre.objects.create(name='fantasy')
        Genre.objects.create(name='history')

    def test_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEquals(max_length, 13)

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEquals(field_label, 'ISBN')

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(book.get_absolute_url(), '/catalog/book/1')

    def test_object_name_is_title_name(self):
        book = Book.objects.get(id=1)
        expected_object_name = book.title
        self.assertEquals(expected_object_name, str(book))

    def test_display_genre(self):
        book = Book.objects.get(id=1)
        genre1 = Genre.objects.get(id=1)
        genre2 = Genre.objects.get(id=2)
        book.genre.add(genre1, genre2)
        expected_genre_list = book.display_genre()
        self.assertEquals(expected_genre_list, 'fantasy, history')

