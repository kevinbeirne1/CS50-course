from django import forms


class PageMarkdownForm(forms.Form):
    page_markdown = forms.CharField(label="Page Markdown")

    def clean_page_markdown(self):
        return self.cleaned_data['page_markdown'].capitalize()


class SearchForm(forms.Form):
    search_name = forms.CharField(label="Search")

    def clean_search_name(self):
        return self.cleaned_data['search_name'].capitalize()


class NewEntryForms(forms.Form):
    entry_name = forms.CharField()
    entry_markdown = forms.CharField(widget=forms.Textarea())

    def clean_entry_name(self):
        return self.cleaned_data['entry_name'].capitalize()

    # def clean_page_markdown(self):
    #     return self.cleaned_data['page_markdown'].capitalize()
