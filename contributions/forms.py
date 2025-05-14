from django import forms
import json
from .models import Contribution
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

class ContributionForm(forms.ModelForm):
    categories_json = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Contribution
        fields = ['date', 'mode_of_payment', 'reference_code', 'categories']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'categories': forms.HiddenInput(),
        }

    # In contributions/forms.py (update the FormHelper layout)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('date', css_class='form-control'),
            Field('mode_of_payment', css_class='form-control', onchange='toggleReferenceCode()'),
            Div(Field('reference_code', css_class='form-control'), css_id='div_id_reference_code', style='display:none;'),  # Add default hidden style
        )
        self.helper.layout.append(Field('categories_json', css_id='id_categories_json'))
        self.helper.layout.append(Field('categories', css_id='id_categories'))


    def clean(self):
        cleaned_data = super().clean()
        categories_json = cleaned_data.get('categories_json')

        print("DEBUG: categories_json =", categories_json)  # Debugging

        if categories_json:
            try:
                categories = json.loads(categories_json)
                print("DEBUG: Parsed categories =", categories)  # Debugging

                if not categories:  
                    self.add_error('categories', "Please provide at least one category and amount.")
                else:
                    self.cleaned_data['categories'] = categories  # Assign the parsed data to the `categories` field

            except json.JSONDecodeError:
                self.add_error('categories_json', "Invalid categories data.")
        else:
            self.add_error('categories', "Categories are required.")

        print("DEBUG: Final cleaned_data =", cleaned_data)  # Debugging
        return cleaned_data
