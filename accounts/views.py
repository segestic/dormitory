from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import StudentSignUpForm, WardenSignUpForm, StudentDetailsForm, SelectionForm, DuesForm, NoDuesForm, RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Student, Room, Hostel, Course
#external.................
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, student_only, warden_only


def index(request):
    return render(request, '../templates/indexnew.html')

@unauthenticated_user
def register(request):
    return render(request, '../templates/register.html')

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '../templates/student_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('edit')


class warden_register(CreateView):
    model = User
    form_class = WardenSignUpForm
    template_name = '../templates/warden_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('warden_student_list')

@login_required
def student_land(request):
    return render(request, '../templates/student_land.html')

# @login_required
# def warden_land(request):
#     return render(request, '../templates/warden_land.html')

def warden_land(request):
    if request.user.is_authenticated:
        if request.user.is_warden:
            return render(request, '../templates/warden_land.html')
            # return redirect('warden_land')
            # return HttpResponseRedirect('/warden_land')
        else:
            # return HttpResponse('You are not authorized to view this page')
            # return HttpResponse('/student_land.html')
            return redirect('student_land')
    else:
        return redirect('login')
    # return render(request, '../templates/index.html')

@unauthenticated_user
def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_student:
                login(request,user)
                return redirect('profile')
            elif user is not None and user.is_warden:
                login(request, user)
                return redirect('warden_student_list')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

#------------------------others-----------------------------
@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            student = request.user.student
            return render(request, 'profile.html', {'student': student})
        else:
            return HttpResponse('not valid')
    else:
        form = RegistrationForm(instance=request.user.student)
    return render(request, 'edit.html', {'form': form})


@login_required
def select(request):
    if request.user.student.room:
        return HttpResponse('You have already selected room - ' + str(request.user.student.room) + '. Please contact your Hostel Caretaker or Warden')

    if request.method == 'POST':
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                request.user.student.room_allotted = True
                room_id = request.user.student.room_id
                room = Room.objects.get(id=room_id)
                room.vacant = False
                room.save()
            form.save()
            student = request.user.student
            return render(request, 'profile.html', {'student': student})
    else:
        try:
            if not request.user.student.no_dues:
                return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
            form = SelectionForm(instance=request.user.student)
            student_gender = request.user.student.gender
            student_course = request.user.student.course
            student_room_type = request.user.student.course.room_type
            hostel = Hostel.objects.filter(
                gender=student_gender)
            # filtered_rooms = Room.objects.all()
            filter1 = Room.objects.none()
            for i in range(len(hostel)):
                h_id = hostel[i].id
            filter2 = Room.objects.filter(hostel_id=h_id, vacant=True)
            filtered_rooms = filter1|filter2
            ###########
            if student_room_type == 'B':
                for i in range(len(hostel)):
                    h_id = hostel[i].id
                    filtered_room = Room.objects.filter(
                        hostel_id=h_id, room_type=['S', 'D'], vacant=True)
                    filtered_rooms = filtered_rooms | filtered_room
            else :
                #for loop to number the lenght of hostels if 10 hostels each of them have numbers
                #len function is used to get the total number of items in list, dictionary e.g 10 etc.
                # range(len)is to create a sequence of numbers from 0 up to len-1 e.g in this case 10 - 1 = 9
                for i in range(len(hostel)):
                    # hostel[i].id is used to get the hostel id i.e
                    #here hostel id will be default numbers 0 - 9,
                    #here it is getting each instance(building) of hostel unique by number
                    # fuulstop(.) is used to get/narrow_down in python
                    h_id = hostel[i].id
                    #filter the roooms according to the parameters - length of hostel, room type and it should be vacant
                    filtered_room = Room.objects.filter(
                        hostel_id=h_id, room_type=student_room_type, vacant=True)
                    #bitwise OR in python that is filtered rooms should be concatenation of the two
                    filtered_rooms = filtered_rooms | filtered_room
            #to get a queryset into a forms field, see it as queryset = filtered_rooms
            #but we will not use a for loop to put it dislay it on template rather we want it as dropdown in form
            form.fields["room"].queryset = filtered_rooms
        except AttributeError:
            return HttpResponse('You cannot select a room because you have not updated your profile')
        return render(request, 'select_room.html', {'form': form})


@login_required
def warden_dues(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = Student.objects.all()
            return render(request, 'dues.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


@login_required
def warden_add_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = DuesForm(request.POST)
                if form.is_valid():
                    student = form.cleaned_data.get('choice')
                    student.no_dues = False
                    student.save()
                    return HttpResponse('Done')
            else:
                form = DuesForm()
                return render(request, 'add_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')

#warden implemented
@login_required
def warden_remove_due(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            if request.method == "POST":
                form = NoDuesForm(request.POST)
                if form.is_valid():
                    #get queryset where choice selected into the variable student and populate it since every field in a
                    #every field has its brother fields, because a database field belongs to an unbreakable/brother record.
                    student = form.cleaned_data.get('choice')
                    student.no_dues = True
                    student.save()
                    return HttpResponse('Done')
            else:
                form = NoDuesForm()
                return render(request, 'remove_due.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')


def logout_view(request):
    logout(request)
    return redirect('/')


def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel)}
    return render(request, 'hostels.html', context)


@login_required
def warden_student_list(request):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            students = Student.objects.all
            # students = []
            # for course in user.warden.hostel.course.all():
                # if course is not None:
                # students = students + list(Student.objects.all())
                # students = students + list(Student.objects.all().filter(course=course))
            return render(request, 'warden_student_list.html', {'students': students})
    else:
        return HttpResponse('Invalid Login')


@login_required
def change_student_details(request, enrollment_no):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            try:
                this_student = Student.objects.get(enrollment_no=enrollment_no)
                #in preparation for change/swap, get the current room id in temp variable old_room_id
                old_room_id = this_student.room_id
            except BaseException:
                raise Http404("Invalid Student or Room")
            if request.method == 'POST':
                #instantiate the form with the prvious id - this_student
                form = StudentDetailsForm(request.POST, instance=this_student)
                if form.is_valid():
                    #nested loop here, if form is valid and below: if room is not null
                    # if this_student.room_id  is None: i.e if we have nothing in the database| not form but database
                    try:
                        if old_room_id is None:
                            print("newly added")
                            #we are combing two tables here, the student table and the room table
                            #the student table is in temp variable this_student. from the Student.objects table;
                            #and the room table Room.object.* stored in the new_room temporal variable
                            #in the next line new_room is the object gotten from the form. i.e the one the user (warden) enters
                            #in other words [this if function will ]get (populate database) from the users input if nothing is in the database
                            new_room = Room.objects.get(id=this_student.room_id)
                            new_room.vacant = False
                            this_student.room_allotted = True
                            # here save both inputs now. the new contents added to the two tables should be saved
                            new_room.save()
                            this_student.save()
                            return redirect('warden_student_list')
                            #if the previous old room id is not equal to this new id
                            # i.e if the room_id input in the student table in database is different from the new one we just got from form
                            #N.B old_room_id is a temporal variable to save the initial value in the student database
                            #if Student.objects.get(enrollment_no=enrollment_no).room_id !=
    #if temp != this_student.room_id
                        elif old_room_id != this_student.room_id:
                            #i.e we are still compareing within the same field in the same table
                            #if value in the room_id of the student table is different from the new value posted into the same field
                            # Free the old room
                            print("switch")
                            #first: select in room table WHERE room table id = student table foreign key, room id
                            #then put the content of the room table; into temporary variable
                            old_room = Room.objects.get(id=old_room_id)
                            #after selecting it via the student foreign key. we begin to populate the room table NOT student table
                            # i.e the old foreign key, row in the table is now vacant
                            old_room.vacant = True
                            old_room.save()
                            #compare Room.objects.get(id=old_room_id) vs Room.objects.get(id=this_student.room_id)
                            #i.e get into a temp variable(old_room) what is inside the room table
                            ##### Allot new room ##########
                            #get select from room table where room id = student room_id (foreign key)
                            #select the new row /foreign key row/record in database we want to populate [optional put it in a variable new_room] and populate
                            new_room = Room.objects.get(id=this_student.room_id)
                            new_room.vacant = False
                            this_student.room_allotted = True
                            # this_student.room_id = new_room.id
                            # user.student.room_allotted = True
                            new_room.save()
                            this_student.save()
                            return redirect('warden_student_list')
                        elif old_room_id == this_student.room_id:
                            #here we are reupdating it even thought it contains the same value as before
                            #we are doing this to preven errors - as a beginner programmer
                            ##### Allot new room [WHICH IS SAME AS PREVIOUS ROOM]##########
                            new_room = Room.objects.get(id=this_student.room_id)
                            new_room.vacant = False
                            this_student.room_allotted = True
                            # this_student.room_id = new_room.id
                            # user.student.room_allotted = True
                            new_room.save()
                            this_student.save()
                            # added recnt
                            # messages.error('Room is same as previous')
                            return redirect('warden_dues')
                        # elif this_student.room_id is None:
                        #     old_room = Room.objects.get(id=old_room_id)
                        #     old_room.vacant = True
                        #     this_student.room_allotted = False
                        #     old_room.save()
                        #     this_student.save()
                        #     return redirect('warden_dues')
                        form = StudentDetailsForm(instance=this_student)
                        form.fields["room"].queryset = Room.objects.filter(vacant=True) | Room.objects.filter(id=this_student.room_id)
                    except Room.DoesNotExist:
                        pass
                return render(request, 'change_student_details.html', {'form': form})

            else:
                form = StudentDetailsForm(instance=this_student)
                form.fields["room"].queryset = Room.objects.filter(vacant=True) | Room.objects.filter(
                    id=this_student.room_id)
                return render(request, 'change_student_details.html', {'form': form})
    else:
        return HttpResponse('Invalid Login')

#############################
@login_required
def clear_room_details(request, enrollment_no):
    user = request.user
    if user is not None:
        if not user.is_warden:
            return HttpResponse('Invalid Login')
        else:
            try:
                this_student = Student.objects.get(enrollment_no=enrollment_no)
                #in preparation for change/swap, get the current room id in temp variable old_room_id
                old_room_id = this_student.room_id
            except BaseException:
                raise Http404("Invalid Student or Room")
            if request.method == 'POST':
                #Get queryset of student this_student
                this_student = Student.objects.get(enrollment_no=enrollment_no)
                try:
                    print("clear")
                    #room queryset is first selected and cleared here
                    room = Room.objects.get(id=this_student.room_id)
                    room.vacant = True
                    #student queryset is cleared here
                    this_student.room_id = None
                    this_student.room_allotted = False
                    # here save both inputs now. the new contents added to the two tables should be saved
                    room.save()
                    this_student.save()
                    return redirect('warden_student_list')
                except Room.DoesNotExist:
                    pass
            return render(request, 'clear_room.html')
    else:
        return HttpResponse('Invalid Login')
