from collections import defaultdict

from django.core.exceptions import ValidationError


class ActivityValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()

        clean_data = self.data

        title = clean_data.get('title')
        description = clean_data.get('description')

        if title == description:
            self.errors['title'].append(
                "O título não pode ser igual a descrição")
            self.errors['description'].append(
                "A descrição não pode ser igual ao título")

        if self.errors:
            raise self.ErrorClass(
                self.errors  # type: ignore
            )

    def clean_title(self, *args, **kwargs):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append(
                "O título precisa ter um mínimo de 5 caracteres")

        return title
