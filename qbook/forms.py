from django import forms

SORT_TAGS = [
    ('N', 'Date added(newest)'),
    ('P', 'Most popular'),
    ('O', 'Date added(oldest)'),


]


class SortForm(forms.Form):
    tag = forms.ChoiceField(choices=SORT_TAGS)
