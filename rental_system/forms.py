from django import forms
from .models import User, Bicycle, RentalRecord, MaintenanceRecord

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="输入密码")

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class RentBicycleForm(forms.Form):
    bicycle = forms.ModelChoiceField(queryset=Bicycle.objects.filter(status='available'))

class ReturnBicycleForm(forms.Form):
    record = forms.ModelChoiceField(queryset=RentalRecord.objects.filter(return_time=None))

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['bicycle', 'maintenance_description']