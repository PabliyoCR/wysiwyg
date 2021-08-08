from django.db import models


def default_sections_order():
    return {"order": [], "selected": ""}

def default_notes_order():
    return {"order": [], "selected": ""}

def default_note_content():
    return {"editor": "", "showEditor": False}

class Category(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title


class Notebook(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    icon = models.CharField(max_length=100, null=True, blank=True)
    sections_order = models.JSONField(null=True, blank=True, default=default_sections_order)
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    notebook = models.ForeignKey(Notebook, null=True, blank=True, on_delete=models.SET_NULL)
    notes_order = models.JSONField(null=True, blank=True, default=default_notes_order)

    def __str__(self):
        return  str(self.notebook) + "/" + self.title


class Note(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.JSONField(null=True, blank=True, default=default_note_content)
    section = models.ForeignKey(Section, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.section) + "/" + self.title
