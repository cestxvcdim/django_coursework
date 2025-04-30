from django import forms

from mailing.models import Client, Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs.update({'class': 'form-check_input'})
            elif isinstance(field, forms.DateTimeField):
                field.widget = forms.DateTimeInput(
                    attrs={
                        'type': 'datetime-local',
                        'class': 'form-control'
                    },
                    format='%Y-%m-%d %H:%M:%S'
                )
                field.input_formats = ['%Y-%m-%d %H:%M:%S']
            else:
                field.widget.attrs.update({'class': 'form-control'})


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user', )


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('creator', 'status',)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('author',)
