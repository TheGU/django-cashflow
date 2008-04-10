from django import newforms as forms
from models import *

__all__ = ('AccountForm', 'TransactionForm', 'MoveMoneyForm', 'FilterHistoryForm', )

def add_empty_label(choices, empty_label=u''):
    a = list(choices)
    a.insert(0, ('', empty_label))
    return tuple(a) 

#TODO: clean_number(check exist/not exist)
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ('user',)

        
class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=add_empty_label(TX_TAG_CHOICES)), required=False)
    description = forms.CharField(widget=forms.Textarea())


class MoveMoneyForm(forms.Form):
    
    def __init__(self, data=None, from_account=None, *arg, **kwarg):
        self.base_fields['account'].queryset = Account.objects\
                            .filter(balance_currency=from_account.balance_currency)\
                            .exclude(number__exact=from_account.number)
        super(MoveMoneyForm, self).__init__(data, *arg, **kwarg)

    account = forms.ModelChoiceField(None)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    tag = forms.IntegerField(widget=forms.Select(choices=add_empty_label(TX_TAG_CHOICES)), required=False)
    description = forms.CharField(widget=forms.Textarea())


class FilterHistoryForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    keywords = forms.CharField(required=False)
