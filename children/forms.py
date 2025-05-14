from django import forms
from members.models import Members
from children.models import Children

class ChildForm(forms.ModelForm):
    father_id = forms.CharField(max_length=50, required=False, label="Father's Unique ID")
    mother_id = forms.CharField(max_length=50, required=False, label="Mother's Unique ID")

    class Meta:
        model = Children
        fields = ['first_name', 'middle_name', 'gender', 'date_of_birth', 'father', 'mother']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'father': forms.HiddenInput(),  # Hide the actual ForeignKey field
            'mother': forms.HiddenInput(),  # Hide the actual ForeignKey field
        }

    def clean(self):
        cleaned_data = super().clean()
        father_id = cleaned_data.get("father_id")
        mother_id = cleaned_data.get("mother_id")

        # Validate father
        father = None
        if father_id:
            father = Members.objects.filter(unique_id=father_id, gender__iexact="Male").first()
            if not father:
                raise forms.ValidationError(f"No male member found with unique_id {father_id}.")
            cleaned_data['father'] = father

        # Validate mother
        mother = None
        if mother_id:
            mother = Members.objects.filter(unique_id=mother_id, gender__iexact="Female").first()
            if not mother:
                raise forms.ValidationError(f"No female member found with unique_id {mother_id}.")
            cleaned_data['mother'] = mother

        # Ensure at least one parent is provided
        if not father and not mother:
            raise forms.ValidationError("At least one parent must be a registered member.")

        return cleaned_data