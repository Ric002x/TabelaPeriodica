import mimetypes
from collections import defaultdict

import fitz
from django.core.exceptions import ValidationError


class ActivityValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        try:
            self.clean_file()
        except TypeError:
            ...

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

    def clean_file(self, *args, **kwargs):
        file = self.data.get('file')

        if file and not file.name.endswith('.pdf'):
            self.errors['file'].append(
                "Você deve enviar um arquivo do tipo PDF"
            )
            return file

        if file:
            file_mime_type, _ = mimetypes.guess_type(file.name)
            if file_mime_type != 'application/pdf':
                self.errors['file'].append(
                    "Você deve enviar um arquivo do tipo PDF"
                )
                return file

        try:
            # Abrindo arquivo do tipo InMemoryUpdatedFile
            with fitz.open(stream=file.read(), filetype="pdf") as pdf:
                if pdf.page_count == 0:
                    self.errors['file'].append(
                        "O PDF enviado está vazio ou corrompido.")
        except Exception:
            if file:
                self.errors['file'].append(
                    "Erro ao processar o arquivo PDF: arquivo inválido")
