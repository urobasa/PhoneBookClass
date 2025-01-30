from model import Phonebook, FileHandler, Contact
from view import ConsoleView
import json

class PhonebookController:
    def __init__(self):
        self.phonebook = Phonebook()
        self.view = ConsoleView()
        self.file_handler = FileHandler()
        self.filename = None

    def run(self):
        while True:
            self.view.show_menu()
            selected_menu = self.view.get_user_input('Введите номер пункта меню: ')
            self.handle_menu(selected_menu)

    def handle_menu(self, selected_menu):
        match selected_menu:
            case '1':
                self.open_file()
            case '2':
                self.save_file()
            case '3':
                self.show_all_contacts()
            case '4':
                self.create_contact()
            case '5':
                self.search_contacts()
            case '6':
                self.edit_contact()
            case '7':
                self.delete_contact()
            case '8':
                self.exit()
            case _:
                self.view.show_message('Выберите один из пунктов меню и введите цифру')
                self.view.press_enter_to_continue()

    def open_file(self):
        while True:
            self.filename = self.view.get_user_input('Введите имя файла или нажмите enter для открытия файла phonebook.json: ')
            self.filename = self.filename if self.filename != "" else 'phonebook.json'
            contacts_data = self.file_handler.open_file(self.filename)
            if contacts_data is not None:
                self.phonebook.contacts = [Contact.from_dict(c) for c in contacts_data]
                if contacts_data:
                    self.view.show_file_status(self.filename, "loaded")
                else:
                    self.view.show_file_status(self.filename, "empty")
                self.view.press_enter_to_continue()
                break
            else:
                crea_fil = self.view.get_user_input('Файл не найден, создать новый файл? y/n ').lower().strip()
                if crea_fil == 'y':
                    with open(self.filename, 'w', encoding='utf-8') as file_cre:
                        json.dump([], file_cre, ensure_ascii=False, indent=4)
                    self.view.show_file_status(self.filename, "new")
                    self.view.press_enter_to_continue()
                    break
                elif crea_fil == 'n':
                    break
                else:
                    self.view.show_message('Введите y/n')

    def save_file(self):
        if self.filename:
            self.file_handler.save_file(self.filename, self.phonebook.contacts)
            self.view.show_file_status(self.filename, "saved")
            self.view.press_enter_to_continue()
        else:
            self.view.show_message('Не открыт файл телефонной книги')
            self.view.press_enter_to_continue()


    def show_all_contacts(self):
        contacts = self.phonebook.get_all_contacts()
        self.view.show_contacts(contacts)
        self.view.press_enter_to_continue()

    def create_contact(self):
        name = self.view.get_user_input('Имя: ')
        while True:
            phone = self.view.get_user_input('Телефон: ')
            if self.view.validate_phone(phone):
                break
            else:
                self.view.show_message('Телефон должен начинаться с + и/или содержать только цифры')
        comment = self.view.get_user_input('Комментарий: ')
        new_contact = Contact(
            id=self._generate_id(),
            name=name,
            phone=phone,
            comment=comment
        )
        self.phonebook.add_contact(new_contact)
        self.view.show_contact_added(new_contact.id)
        self.view.press_enter_to_continue()

    def search_contacts(self):
        query = self.view.get_user_input('Введите текст для поиска: ')
        if query:
            found_contacts = self.phonebook.search_contacts(query)
            if found_contacts:
                self.view.show_contacts(found_contacts)
            else:
                self.view.show_message('Не найдены')
            self.view.press_enter_to_continue()
        else:
            self.view.show_message('Введен пустой поисковый запрос')
            self.view.press_enter_to_continue()

    def edit_contact(self):
        contact_id = int(self.view.get_user_input('ID контакта для редактирования: '))
        contact = self.phonebook.get_contact_by_id(contact_id)
        if contact:
            new_name = self.view.get_user_input(f'Изменить имя - {contact.name}: ')
            while True:
                new_phone = self.view.get_user_input(f'Изменить телефон - {contact.phone}: ')
                if new_phone == "" or self.view.validate_phone(new_phone):
                    break
                else:
                    self.view.show_message('Телефон должен начинаться с + и/или содержать только цифры')
            new_comment = self.view.get_user_input(f'Изменить коммент - {contact.comment}: ')

            # Если поле не введено, оставляем старое значение
            if new_name:
                contact.name = new_name
            if new_phone:
                contact.phone = new_phone
            if new_comment:
                contact.comment = new_comment

            self.view.show_message("Контакт успешно изменен.")
            self.view.press_enter_to_continue()
        else:
            self.view.show_message("Контакт с таким ID не найден.")
            self.view.press_enter_to_continue()

    def delete_contact(self):
        contact_id = int(self.view.get_user_input('ID контакта для удаления: '))
        contact = self.phonebook.get_contact_by_id(contact_id)
        if contact:
            self.phonebook.delete_contact(contact_id)
            self.view.show_contact_deleted(contact)
            self.view.press_enter_to_continue()
        else:
            self.view.show_message("Контакт с таким ID не найден.")
            self.view.press_enter_to_continue()

    def exit(self):
        if self.filename and self.file_handler.are_contacts_different(self.filename, self.phonebook.contacts):
            if self.view.ask_to_save_changes(self.filename):
                self.file_handler.save_file(self.filename, self.phonebook.contacts)
        self.view.show_message('Программа завершена')
        self.view.press_enter_to_continue()
        exit()

    def _generate_id(self):
        if self.phonebook.contacts:
            return max(c.id for c in self.phonebook.contacts) + 1
        return 1

