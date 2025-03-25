import pickle
from address_book_module import AddressBook, Record
from notes_module import NoteBook
from ui_helpers import (
    print_title,
    print_info,
    print_success,
    print_error,
    print_warning,
    show_command_help,
    show_contacts_table,
    show_notes_table
)

BOOK_FILE = "addressbook.pkl"
NOTES_FILE = "notebook.pkl"

address_book = None
notebook = None

def main():
    global address_book, notebook
    address_book = load_data(BOOK_FILE, AddressBook)
    notebook = load_data(NOTES_FILE, NoteBook)

    print_title("PERSONAL ASSISTANT BOT 🤖")
    show_command_help()

    commands = {
        "hello": greet,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "delete": delete_contact,
        "add-note": add_note,
        "search-notes": search_notes,
        "edit-note": edit_note,
        "delete-note": delete_note,
        "show-notes": show_notes,
        "add-tag": add_tag,
        "remove-tag": remove_tag,
        "search-tag": search_by_tag,
        "exit": goodbye,
        "close": goodbye
    }

    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue
        try:
            cmd, *args = parse_input(user_input)
            if cmd in commands:
                result = commands[cmd](*args)
                if result:
                    print_info(result)
                if cmd in ("exit", "close"):
                    save_data(address_book, BOOK_FILE)
                    save_data(notebook, NOTES_FILE)
                    break
            else:
                print_warning("Invalid command. Available commands:")
                show_command_help()
        except Exception as e:
            print_error(f"Error: {e}")

def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0].lower(), *parts[1:]

def input_error(ValueErrorMessage="Invalid input.", IndexErrorMessage="Missing arguments.", KeyErrorMessage="Key error"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError:
                return ValueErrorMessage
            except IndexError:
                return IndexErrorMessage
            except KeyError:
                return KeyErrorMessage
        return wrapper
    return decorator

@input_error("Please provide name and phone.")
def add_contact(name, phone):
    if address_book.find(name):
        return f"Contact {name} already exists."
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact {name} added."

@input_error("Please provide name, old phone and new phone.")
def change_contact(name, old_phone, new_phone):
    contact = address_book.find(name)
    if not contact:
        return "Contact not found."
    contact.edit_phone(old_phone, new_phone)
    return f"Phone {old_phone} changed to {new_phone} for {name}."

@input_error("Please provide a name.")
def show_phone(name):
    contact = address_book.find(name)
    if not contact:
        return "Contact not found."
    return ", ".join(p.value for p in contact.phones)

@input_error("Please provide name and birthday.")
def add_birthday(name, birthday):
    contact = address_book.find(name)
    if not contact:
        return "Contact not found."
    contact.add_birthday(birthday)
    return "Birthday added."

@input_error("Please provide a name.")
def show_birthday(name):
    contact = address_book.find(name)
    if not contact:
        return "Contact not found."
    return contact.birthday.value.strftime("%d.%m.%Y") if contact.birthday else "Birthday not set"

def birthdays():
    upcoming = address_book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{item['name']} - {item['congratulation_date']}" for item in upcoming])

def show_all():
    if not address_book.data:
        return "No contacts found."
    show_contacts_table(address_book.values())
    return None

@input_error("Please provide a name.")
def delete_contact(name):
    if address_book.delete(name):
        return f"Contact {name} deleted."
    return "Contact not found."

@input_error("Please provide a note body.")
def add_note(*text):
    body = " ".join(text)
    note = notebook.add_note(body)
    return f"Note added: {note.text[:30]}..."

@input_error("Please provide a keyword to search.")
def search_notes(keyword):
    results = notebook.search_notes(keyword)
    if not results:
        return "No matching notes found."
    show_notes_table(results)
    return None

@input_error("Please provide a note ID and new body.")
def edit_note(note_id_str, *new_body_parts):
    note_id = int(note_id_str)
    new_body = " ".join(new_body_parts)
    if notebook.edit_note(note_id, new_body):
        return "Note updated."
    return "Note not found."

@input_error("Please provide a note ID.")
def delete_note(note_id_str):
    note_id = int(note_id_str)
    if notebook.delete_note(note_id):
        return "Note deleted."
    return "Note not found."

def show_notes():
    notes = notebook.get_all_notes()
    if not notes:
        return "No notes found."
    show_notes_table(notes)
    return None

@input_error("Please provide a note ID and tag.")
def add_tag(note_id_str, tag):
    note_id = int(note_id_str)
    if notebook.add_tag_to_note(note_id, tag):
        return f"Tag '{tag}' added to note {note_id}."
    return "Note not found."

@input_error("Please provide a note ID and tag.")
def remove_tag(note_id_str, tag):
    note_id = int(note_id_str)
    if notebook.remove_tag_from_note(note_id, tag):
        return f"Tag '{tag}' removed from note {note_id}."
    return "Note not found."

@input_error("Please provide a tag to search.")
def search_by_tag(tag):
    results = notebook.search_by_tag(tag)
    if not results:
        return "No notes with that tag found."
    show_notes_table(results)
    return None

def greet():
    return "How can I help you?"

def goodbye():
    return "Goodbye!"

def save_data(data, filename):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data(filename, default_class):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default_class()

if __name__ == "__main__":
    main()

