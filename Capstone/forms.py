from django import forms

class CheckoutForm(forms.Form):
    
    house_num = forms.CharField(label='Flat Number/Door Number',required=True,widget=forms.TextInput(attrs={'placeholder':'Flat Number/Door Number','class':'form-control required'})) 
    address_line1 = forms.CharField(label='Address line 1',required=True,widget=forms.TextInput(attrs={'class':'form-control required','placeholder':'Flat name/Street name'}))
    address_line2 = forms.CharField(label='Address line 2',required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Area/Colony'}))
    landmark = forms.CharField(label='Landmark (Optional)',required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Landmark'}))
    city = forms.CharField(label='City',required=True,widget=forms.TextInput(attrs={'class':'form-control required'}))
    state = forms.CharField(label='State',required=True,widget=forms.TextInput(attrs={'class':'form-control required'}))
    pincode = forms.CharField(label='PinCode',required=True,widget=forms.TextInput(attrs={'class':'form-control required'}))
    mobile_number = forms.CharField(label='Contact Number',required=True,widget=forms.TextInput(attrs={'class':'form-control required'}))

class LoginForm(forms.Form):
    
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control','name':'next'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))

class RegisterForm(forms.Form):

    username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    confirmation = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control'}))
