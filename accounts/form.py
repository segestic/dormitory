from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Student, Warden


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    enrollment_no = forms.CharField(required=True, max_length=5, help_text="Enter your 5 digits Student Number.")

    def clean_enrollment_no(self):
        enrollment_no = self.cleaned_data.get('enrollment_no')
        if len(enrollment_no) < 5:
            raise forms.ValidationError("Enrollment number must be at least 5 digits.")
        if Student.objects.filter(enrollment_no=enrollment_no).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Enrollment number exists.')
        return enrollment_no

    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        #get user data from the upper parent (super class) and save temporarily
        user = super().save(commit=False)
        #in addition to the data gotten from super class, record True into the .is_student field/column
        user.is_student = True
        #in addition get the firstname and lastname of user from the form (cleaned form)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        #save the changes into user instance- i.e the super, student True, first_name, last_name
        user.save()
        #create a student instance object from the data saved into user(variable)
        student = Student.objects.create(user=user)
        #get student enrollment data from the form and clean it
        # Student.enrollment_no = ['enrollment_no'].clean_enrollment_no
        student.enrollment_no = self.cleaned_data.get('enrollment_no')
        # Student.enrollment_no = self.clean_enrollment_no()
        #now save the student enrollment number into the student instance/record.
        student.save()
        #return user
        return user


class WardenSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_warden = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        User.gender = self.cleaned_data.get('gender')
        User.course = self.cleaned_data.get('course')
        user.save()
        warden = Warden.objects.create(user=user)
        warden.save()
        return user


class StudentDetailsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['enrollment_no', 'room', 'course', 'dob', 'no_dues']

# class UpdateForm(forms.ModelForm:
#     class Meta:
#         model = Student

class SelectionForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['room']


class DuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=True))


class NoDuesForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Student.objects.all().filter(no_dues=False))

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            # 'first_name',
            # 'last_name',
            'enrollment_no',
            'course',
            'dob',
            'gender']
