from django import forms
from ..models import ActivityRating


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label='',
        required=True,
        error_messages={
            'required': 'selecione um valor para avaliação'
        },
        widget=forms.RadioSelect,
        choices=((1, '1 star'), (2, '2 star'), (3, '3 star'),
                 (4, '4 star'), (5, '5 star')))

    class Meta:
        model = ActivityRating
        fields = ['rating', 'comment']
