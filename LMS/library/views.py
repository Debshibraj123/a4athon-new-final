from django.shortcuts import render, redirect,HttpResponse
from .forms import StudentsForm, BookForm, Book_IssueForm,Book_instanceForm
from .models import Students, Book, Book_Issue,BookInstance
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User



@login_required(login_url='login')
def index(request):
    return(render(request, 'index.html'))

@login_required(login_url='login')
def add_new_student(request):
    if request.method=="POST":
        form = StudentsForm((request.POST))
        if form.is_valid():
            form.save()
            return redirect('/show_students')
    else:
        form = StudentsForm
    return (render(request, 'add_new_student.html', {'form':form}))

@login_required(login_url='login')
def add_new_book(request):
    if request.method=="POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form=form.save()
            book_instance=BookInstance(book=form)
            book_instance.save()
            return redirect('/view_books')
    else:
        form = BookForm
        form_instance=Book_instanceForm
        return (render(request, 'add_new_book.html', {'form':form,"form_instance":form_instance}))

@login_required(login_url='login')
def add_new_book_instance(request):
    form=Book_instanceForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('/view_books')

@login_required(login_url='login')
def add_book_issue(request):
    if request.method=="POST":
        form = Book_IssueForm(request.POST)
        if form.is_valid():
            # save data
            unsaved_form=form.save(commit=False)
            book_to_save=BookInstance.objects.get(id=unsaved_form.book_instance.id)
            book_to_save.Is_borrowed=True
            book_to_save.save()
            form.save()
            form.save_m2m()
        return redirect('/view_books_issued')
    else:
        context={'form':Book_IssueForm,"book":BookInstance.objects.filter(Is_borrowed=False)}
        return render(request, 'add_book_issue.html',context=context)

@login_required(login_url='login')
def view_students(request):
    students = Students.objects.order_by('-id')
    return render(request,'view_students.html', {'students': students})

@login_required(login_url='login')
def view_books(request):
    books=BookInstance.objects.order_by('id')
    return render(request,'view_books.html', {'books': books})

@login_required(login_url='login')
def view_bissue(request):
    issue = Book_Issue.objects.order_by('-id')
    return render(request,'issue_records.html', {'issue': issue})

@login_required(login_url='login')
def edit_student_data(request,roll):
    try:
        if request.method == "POST":
            std=Students.objects.get(id=request.session['id'])    
            form = StudentsForm((request.POST),instance=std)
            if form.is_valid():
                form.save()
            del request.session['id']
            return redirect("/show_students")
        else:
            student_to_edit=Students.objects.get(roll_number=roll)
            student=StudentsForm(instance=student_to_edit)
            request.session["id"]=student_to_edit.id
            return render(request,'edit_student_data.html',{'student':student})
    except Exception as error:
        print(f"{error} occured at edit_student_data view")

@login_required(login_url='login')
def delete_book(request, title):
    try:
        book = Book.objects.get(book_title=title)
        if request.method == "POST":
            book.delete()
            return redirect('/view_books')
        return render(request, 'delete_book.html', {'book': book})
    except Book.DoesNotExist:
        return HttpResponse(f"Book with ID: {id} does not exist.")

@login_required(login_url='login')
def delete_student(request, roll):
    try:
        student = Students.objects.get(roll_number=roll)
        if request.method == "POST":
            student.delete()
            return redirect('/show_students')
        return render(request, 'delete_student.html', {'student': student})
    except Students.DoesNotExist:
        return HttpResponse(f"Student with Roll Number: {roll} does not exist.")

@login_required(login_url='login')
def edit_book(request, id):
    try:
        book = Book.objects.get(id=id)
        if request.method == "POST":
            # Update the book's data
            book.book_title = request.POST['book_title']
            book.author = request.POST['author']
            # Save the changes
            book.save()
            return redirect('/view_books')
        return render(request, 'edit_book.html', {'book': book})
    except Book.DoesNotExist:
        return HttpResponse(f"Book with ID: {id} does not exist.")


def return_issued_book(request,id):   
    obj=Book_Issue.objects.get(id=id)
    return HttpResponse(f"<h2>Return Issued Book</h2><label>Book <i>{obj.book_instance.book.book_title}</i> issued to <i>{obj.student.fullname}</i> could not be returned..</label><h2>The feature is comming soon</h2>")

def edit_issued(request, id):
    obj=Book_Issue.objects.get(id=id)
    return HttpResponse(f"<h2>Edit Issued Book</h2><label>Book <i>{obj.book_instance.book.book_title}</i> issued to <i>{obj.student.fullname}</i> could not be edited..</label><h2>The feature is comming soon</h2>")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('index')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')