import re
import pickle
from datetime import datetime


class Note:
    def __init__(self, id: int, text: str, tags=None):
        self.id = id
        self.text = text
        self.tags = tags if tags else []
        self.created = datetime.now()

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def edit_text(self, new_text):
        self.text = new_text

    def __str__(self):
        tags_str = ', '.join(self.tags) if self.tags else 'No tags'
        return f"[{self.id}] {self.text}\nTags: {tags_str}\nCreated: {self.created.strftime('%Y-%m-%d %H:%M')}"

    def __getstate__(self):
        return {
            'id': self.id,
            'text': self.text,
            'tags': self.tags,
            'created': self.created
        }

    def __setstate__(self, state):
        self.id = state['id']
        self.text = state['text']
        self.tags = state['tags']
        self.created = state['created']


class NoteBook:
    def __init__(self):
        self.notes = []
        self.last_id = 0

    def add_note(self, text, tags=None):
        self.last_id += 1
        note = Note(self.last_id, text, tags)
        self.notes.append(note)
        return note

    def delete_note(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                self.notes.remove(note)
                return True
        return False

    def edit_note(self, note_id, new_text):
        for note in self.notes:
            if note.id == note_id:
                note.edit_text(new_text)
                return True
        return False

    def search_notes(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.text.lower()]

    def search_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    def add_tag_to_note(self, note_id, tag):
        for note in self.notes:
            if note.id == note_id:
                note.add_tag(tag)
                return True
        return False

    def remove_tag_from_note(self, note_id, tag):
        for note in self.notes:
            if note.id == note_id:
                note.remove_tag(tag)
                return True
        return False

    def get_all_notes(self):
        return self.notes

    def __getstate__(self):
        return {
            'notes': self.notes,
            'last_id': self.last_id
        }

    def __setstate__(self, state):
        self.notes = state['notes']
        self.last_id = state['last_id']