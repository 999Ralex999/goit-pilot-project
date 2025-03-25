from colorama import Fore, Style
from rich.console import Console
from rich.table import Table

console = Console()

def print_title(title):
    border = "=" * (len(title) + 10)
    print(Fore.CYAN + border)
    print(f"     {title.upper()}")
    print(border + Style.RESET_ALL)

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)

def print_info(message):
    print(Fore.BLUE + message + Style.RESET_ALL)

def print_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)

def show_command_help():
    print(Fore.MAGENTA + "\nAvailable commands:")
    print("→ add <name> <phone> — Add new contact")
    print("→ change <name> <old_phone> <new_phone> — Edit phone")
    print("→ add-birthday <name> <dd.mm.yyyy> — Add birthday")
    print("→ phone <name> — Show phones")
    print("→ show-birthday <name> — Show birthday")
    print("→ all — Show all contacts")
    print("→ birthdays — Birthdays in next 7 days")
    print("→ add-note <text> — Add note")
    print("→ edit-note <id> <text> — Edit note")
    print("→ delete-note <id> — Delete note")
    print("→ show-notes — Show all notes")
    print("→ add-tag <id> <tag> — Add tag")
    print("→ remove-tag <id> <tag> — Remove tag")
    print("→ search-notes <keyword> — Search in notes")
    print("→ search-tag <tag> — Search by tag")
    print("→ delete <name> — Delete contact")
    print("→ hello — Greet")
    print("→ exit / close — Exit\n" + Style.RESET_ALL)

def show_contacts_table(contacts):
    table = Table(title="CONTACT LIST")
    table.add_column("Name", style="cyan")
    table.add_column("Phones")
    table.add_column("Email")
    table.add_column("Birthday")
    table.add_column("Address")

    for rec in contacts:
        phones = ", ".join(p.value for p in rec.phones) if rec.phones else ""
        email = rec.email.value if rec.email else ""
        birthday = rec.birthday.value.strftime("%d.%m.%Y") if rec.birthday else ""
        address = rec.address.value if rec.address else ""
        table.add_row(rec.name.value, phones, email, birthday, address)

    console.print(table)

def show_notes_table(notes):
    table = Table(title="NOTES")
    table.add_column("ID", style="cyan")
    table.add_column("Text")
    table.add_column("Tags")

    for note in notes:
        tags = ", ".join(note.tags) if note.tags else ""
        table.add_row(str(note.id), note.text, tags)

    console.print(table)