# chatgpt_app/forms.py

from django import forms

class SearchForm(forms.Form):
    """検索フォーム"""
    api_key = forms.CharField(
        label="ChatGPT APIキー",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'sk-...',
            'autocomplete': 'off'
        }),
        required=True
    )
    
    query = forms.CharField(
        label="検索したいこと",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'ここに検索したい内容を入力してください...'
        }),
        required=True
    )

class ExportForm(forms.Form):
    """エクスポートフォーム"""
    filename = forms.CharField(
        label="ファイル名",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'chatgpt_history.json'
        }),
        required=False
    )