from django import  forms
from .models import * 


class AddProducts(forms.ModelForm):
    Product = forms.CharField(widget=forms.TextInput( attrs={'placeholder':'Name of Product',}), label='')
    Desc = forms.CharField(widget=forms.TextInput( attrs={'placeholder':'Description',}), label='')
    Price = forms.DecimalField(widget=forms.NumberInput( attrs={'placeholder':'Price',}), label='')
    Availability =forms.CharField(widget=forms.TextInput( attrs={'value':'available'}), label='')
    Image = forms.ImageField(label='')
    Brand = forms.CharField(widget=forms.TextInput( attrs={'placeholder':'Brand'}), label='')

    class Meta:
        model = Products
        fields = ('Product', 'Desc', 'Availability', 'Price', 'Image', 'Brand')
        widgets = {
         'Product': forms.TextInput( 
                       attrs = {
                           'placeholder':'Name of Product',
                           'class':'productname',
                           'label':''
                       }
                   ),

        'Desc': forms.TextInput( 
                       attrs = {
                           'placeholder':'Description',
                            
                       }
                   ),
        'Availability': forms.TextInput( 
                       attrs = {
                           'placeholder':'Availability',
                           'class':'quantity'
                       }
                   ),
        'Price': forms.TextInput( 
                       attrs = {
                           'placeholder':'Price',
                           'class':'price'
                           
                       }
                   ),
        'Brand': forms.TextInput( 
                       attrs = {
                           'placeholder':'Product Brand',
                           
                       }
                   )

        }

class MyCarts(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('Telephone', 'Product', 'quantity', 'Price', 'Total') 

class PickProducts(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('Product', 'Price')