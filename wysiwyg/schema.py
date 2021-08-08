import graphene
from graphene.types import generic
from graphene_django import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

# Category
class CategoryNode(DjangoObjectType):

    class Meta:
        model = Category
        filter_fields = []
        interfaces = (graphene.relay.Node,)


# Notebook
class NotebookNode(DjangoObjectType):
    sections_order = generic.GenericScalar()

    class Meta:
        model = Notebook
        filter_fields = []
        interfaces = (graphene.relay.Node,)


# Update Section Selected (mutation)
class UpdateSectionSelected(graphene.relay.ClientIDMutation):
    notebook = graphene.Field(NotebookNode)

    class Input:
        notebookID = graphene.String()
        selected = generic.GenericScalar()

    def mutate_and_get_payload(root, info, **input):
        notebook = Notebook.objects.get(pk=from_global_id(input.get('notebookID'))[1])
        notebook.sections_order["selected"] = input.get('selected')
        notebook.save()
        return UpdateSectionSelected(notebook=notebook)


# Update Sections Order (mutation)
class UpdateSectionsOrder(graphene.relay.ClientIDMutation):
    notebook = graphene.Field(NotebookNode)

    class Input:
        notebookID = graphene.String()
        order = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        notebook = Notebook.objects.get(pk=from_global_id(input.get('notebookID'))[1])
        notebook.sections_order["order"] = input.get('order')
        notebook.save()
        return UpdateSectionsOrder(notebook=notebook)


# Section
class SectionNode(DjangoObjectType):
    notes_order = generic.GenericScalar()

    class Meta:
        model = Section
        filter_fields = ['notebook']
        interfaces = (graphene.relay.Node,)


# Create Section
class CreateSection(graphene.relay.ClientIDMutation):
    section = graphene.Field(SectionNode)

    class Input:
        title = graphene.String()
        notebookID = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        notebook = Notebook.objects.get(pk=from_global_id(input.get('notebookID'))[1])
        section = Section(
            title=input.get('title'),
            notebook = notebook
        )
        section.save()
        return CreateSection(section=section)


# Rename Section
class RenameSection(graphene.relay.ClientIDMutation):
    section = graphene.Field(SectionNode)

    class Input:
        sectionID = graphene.String()
        title = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        section = Section.objects.get(pk=from_global_id(input.get('sectionID'))[1])
        section.title = input.get('title')
        section.save()
        return RenameSection(section=section)

# Delete Section
class DeleteSection(graphene.relay.ClientIDMutation):
    section = graphene.Field(SectionNode)

    class Input:
        sectionID = graphene.String()
        notebookID = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        notebook = Notebook.objects.get(pk=from_global_id(input.get('notebookID'))[1])
        if input.get('sectionID') == notebook.sections_order["selected"]:
            notebook.sections_order["selected"] = ""
            print("//////////////")
            print(input.get('sectionID'))
            print(input.get('notebookID'))
            print(notebook.sections_order["selected"])
            notebook.save()
        if input.get('sectionID') in notebook.sections_order["order"]:
            print("SI ESTA //////////////")
            notebook.sections_order["order"].remove(input.get('sectionID'))
            notebook.save()
        else:
            print("NO ESTA //////////////")
        section = Section.objects.get(pk=from_global_id(input.get('sectionID'))[1])
        section.delete()
        return DeleteSection(section=section)


# Update Note Selected (mutation)
class UpdateNoteSelected(graphene.relay.ClientIDMutation):
    section = graphene.Field(SectionNode)

    class Input:
        sectionID = graphene.String()
        selected = generic.GenericScalar()

    def mutate_and_get_payload(root, info, **input):
        section = Section.objects.get(pk=from_global_id(input.get('sectionID'))[1])
        section.notes_order["selected"] = input.get('selected')
        section.save()
        return UpdateNoteSelected(section=section)


#  Update Notes Order (mutation)
class UpdateNotesOrder(graphene.relay.ClientIDMutation):
    section = graphene.Field(SectionNode)

    class Input:
        sectionID = graphene.String()
        order = graphene.List(graphene.String)

    def mutate_and_get_payload(root, info, **input):
        section = Section.objects.get(pk=from_global_id(input.get('sectionID'))[1])
        section.notes_order["order"] = input.get('order')
        section.save()
        return UpdateNotesOrder(section=section)


# Note
class NoteNode(DjangoObjectType):
    content = generic.GenericScalar()

    class Meta:
        model = Note
        filter_fields = ['section']
        interfaces = (graphene.relay.Node,)


# Create Note
class CreateNote(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteNode)

    class Input:
        title = graphene.String()
        sectionID = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        section = Section.objects.get(pk=from_global_id(input.get('sectionID'))[1])
        note = Note(
            title=input.get('title'),
            section = section
        )
        note.save()
        return CreateNote(note=note)


# Rename Note
class RenameNote(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteNode)

    class Input:
        noteID = graphene.String()
        title = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        note = Note.objects.get(pk=from_global_id(input.get('noteID'))[1])
        note.title = input.get('title')
        note.save()
        return RenameNote(note=note)

# Delete Note
class DeleteNote(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteNode)

    class Input:
        noteID = graphene.String()
        sectionID = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        section = Section.objects.get(pk=from_global_id(input.get('sectionID'))[1])
        if input.get('noteID') in section.notes_order["order"]: 
            section.notes_order["order"].remove(input.get('noteID'))
        if input.get('noteID') == section.notes_order["selected"]:
            section.notes_order["selected"] = ""
        section.save()
        note = Note.objects.get(pk=from_global_id(input.get('noteID'))[1])
        note.delete()
        return DeleteNote(note=note)


# Update Note (mutation)
class UpdateNoteEditor(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteNode)

    class Input:
        noteID = graphene.String()
        editor = generic.GenericScalar()

    def mutate_and_get_payload(root, info, **input):
        note = Note.objects.get(pk=from_global_id(input.get('noteID'))[1])
        note.content['editor'] = input.get('editor')
        note.content['showEditor'] = False
        note.save()
        return UpdateNoteEditor(note=note)


class UpdateNoteShowEditor(graphene.relay.ClientIDMutation):
    note = graphene.Field(NoteNode)

    class Input:
        noteID = graphene.String()
        show = graphene.Boolean()

    def mutate_and_get_payload(root, info, **input):
        note = Note.objects.get(pk=from_global_id(input.get('noteID'))[1])
        note.content['showEditor'] = input.get('show')
        note.save()
        return UpdateNoteShowEditor(note=note)


class Query(object):
    notebook = graphene.relay.Node.Field(NotebookNode, id=graphene.String())
    section = graphene.relay.Node.Field(SectionNode, id=graphene.String())
    note = graphene.relay.Node.Field(NoteNode, id=graphene.String())
    all_categories = DjangoFilterConnectionField(CategoryNode)
    all_notebooks = DjangoFilterConnectionField(NotebookNode)
    all_sections = DjangoFilterConnectionField(SectionNode)
    all_notes = DjangoFilterConnectionField(NoteNode)


""" class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryNode)
    all_notebooks = graphene.List(NotebookNode)
    notebook = graphene.relay.Node.Field(NotebookNode, id=graphene.String())
    all_sections = graphene.List(SectionNode, notebook_id=graphene.String())
    all_notes = graphene.List(NoteNode)

    def resolve_all_categories(root, info, **kwargs):
        return Category.objects.all()

    def resolve_all_notebooks(root, info, **kwargs):
        return Notebook.objects.all()

    def resolve_all_sections(root, info, **kwargs):
        notebook_id = kwargs.get('notebook_id')
        notebook = Notebook.objects.get(id=notebook_id)
        print(notebook)
        print("///////////////////////")
        if notebook:
            return Section.objects.filter(notebook=notebook)
        return Section.objects.all()

    def resolve_all_notes(root, info, **kwargs):
        return Note.objects.all() """


class Mutation(graphene.AbstractType):
    update_section_selected = UpdateSectionSelected.Field()
    update_sections_order = UpdateSectionsOrder.Field()
    create_section = CreateSection.Field()
    rename_section = RenameSection.Field()
    delete_section = DeleteSection.Field()
    update_note_selected = UpdateNoteSelected.Field()
    update_notes_order = UpdateNotesOrder.Field()
    create_note = CreateNote.Field()
    rename_note = RenameNote.Field()
    delete_note = DeleteNote.Field()
    update_note_editor = UpdateNoteEditor.Field()
    update_note_show_editor = UpdateNoteShowEditor.Field()
