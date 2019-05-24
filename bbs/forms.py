from django import forms
from .models import Choice, Question


class ChoiceForm(forms.ModelForm):
    choice_text = forms.CharField(
        label="你的答案",
        max_length=2000,
        help_text='最大长度为2000',
        widget=forms.Textarea(
            attrs={
                'placeholder': "请说出你的答案",
                "rows": 8,
                "class": 'form-control'
            }
        )
    )
    picture = forms.FileField(
        label="添加图片(可选)",
        help_text='可以上传的格式: jpg, png',
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": 'form-control'
            }
        )
    )

    class Meta:
        model = Choice
        fields = ['choice_text', 'picture']


class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        label="问题",
        max_length=200,
        help_text='最大长度为200',
        widget=forms.TextInput(
            attrs={
                'placeholder': "请输入想问的话题",
                "class": 'form-control'
            }
        )
    )
    question_desc = forms.CharField(
        label="问题详细描述",
        max_length=800,
        # help_text='内容不超过800',
        widget=forms.Textarea(
            attrs={
                'placeholder': "内容不超过800",
                "class": 'form-control'
            }
        )
    )

    picture = forms.FileField(
        label="添加图片(可选)",
        help_text='可以上传的格式: jpg, png',
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": 'form-control'           
            }
        )
    )

    class Meta:
        model = Question
        fields = ['question_text', 'question_desc', 'picture']