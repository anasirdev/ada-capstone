from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookForm
from .utils import parse_ged, parse_xml
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Book, Person, Name

def home(request):
    names = Name.objects.all()
    male = len(Name.objects.filter(gender="M"))
    female = len(Name.objects.filter(gender="F"))
    len_names = len(names)
    return render(request, 'babynamebook/home.html', {'names': names, 'male': male, 'female': female, 'len_names': len_names})


def get_tree_instructions(request):
    return render(request, 'babynamebook/get_tree_instructions.html', {})


def upload_tree(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book(tree_upload=request.FILES['tree_upload'], title=request.POST['title'])
            # add stuff about user
            book.save()
            filename = book.tree_upload.name
            xml_filename = parse_ged(filename)

            # person_list is an array of dictionary objects
            person_list = parse_xml(xml_filename)
            request.session["book_id"] = book.id
            parse_person(request, person_list)

        return redirect('progress')
    else:
        form = BookForm()
    return render(request, 'babynamebook/upload_tree.html', {'form': form})


def progress(request):
    book = get_object_or_404(Book, id=request.session["book_id"])
    persons = Person.objects.filter(book=book)
    total_persons = len(persons)
    num_m = len(Person.objects.filter(book=book, gender="M"))
    num_f = len(Person.objects.filter(book=book, gender="F"))

    return render(request, 'babynamebook/progress.html', {'book': book, 'persons': persons, 'total_persons': total_persons, 'num_m': num_m, 'num_f': num_f})

def correlate(request):
    book = get_object_or_404(Book, id=request.session["book_id"])
    persons = Person.objects.filter(book=book)

    for p in persons:
        try:
            first = Name.objects.get(first_name = p.first_name, gender=p.gender)
            book.names.add(first)

        except Name.DoesNotExist:
            continue

    for p in persons:
        if p.middle_name != None:
            try:
                middle = Name.objects.get(first_name = p.middle_name, gender=p.gender)
                book.names.add(middle)

            except Name.DoesNotExist:
                continue

    female = book.names.all().filter(gender="F")
    male = book.names.all().filter(gender="M")
    female_a_names = book.names.all().filter(gender="F", first_name__startswith="A").order_by('first_name')




    return render(request, 'babynamebook/correlate.html', {'book': book, 'persons': persons, 'male': male, 'female': female, 'female_a_names': female_a_names})


# this is a private method
def parse_person(request, person_list):
    for p in person_list:
        new_person = Person(first_name=p["first_name"], last_name=p["last_name"], gender=p["sex"], birth_year=p["birth_year"], )

        if p["last_name"] is None:
            new_person.last_name = "unknown"

        if p["sex"] is None:
            new_person.gender = "x"

        if p["birth_year"] is None:
            new_person.birth_year = 0
        book = get_object_or_404(Book, id=request.session["book_id"])

        new_person.book = book
        new_person.save()
