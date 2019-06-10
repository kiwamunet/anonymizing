from django import forms


class UploadFileForm(forms.Form):
    # formのname 属性が 'file' になる
    file = forms.FileField(
        required=True,
        label='CSVファイルを選択してください')

    # add
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.name.endswith('.csv'):
            return file
        else:
            raise forms.ValidationError('拡張子はcsvのみです')
