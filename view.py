class ConsoleView:
    @staticmethod
    def show_menu():
        print("""
        1. Открыть файл
        2. Сохранить файл
        3. Показать все контакты
        4. Создать контакт
        5. Найти контакт
        6. Изменить контакт
        7. Удалить контакт
        8. Выйти
        """)

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    @staticmethod
    def show_message(message):
        print(message)

    @staticmethod
    def press_enter_to_continue():
        input("Нажмите Enter для продолжения...")

    @staticmethod
    def show_contacts(contacts):
        if contacts:
            print('\nКонтакты: ')
            print('-------------------------')
            for cont in contacts:
                print("ID:", cont.id)
                print("Имя:", cont.name)
                print("Тел:", cont.phone)
                print("Коммент:", cont.comment, '\n')
            print('-------------------------')
        else:
            print('Ни одного контакта в списке контактов нет')

    @staticmethod
    def show_file_status(filename, status):
        if status == "loaded":
            print(f'Контакты загружены из файла {filename}')
        elif status == "empty":
            print(f'Открыт файл {filename} не содержащий ни одного контакта')
        elif status == "new":
            print(f'Открыт новый файл справочника {filename}')
        elif status == "saved":
            print(f'Сохранен файл справочника {filename}')

    @staticmethod
    def show_contact_added(contact_id):
        print(f"Контакт добавлен ID:{contact_id}")

    @staticmethod
    def show_contact_deleted(contact):
        print('---------Удален контакт----------')
        print(f"Имя: {contact.name}")
        print(f"Телефон: {contact.phone}")
        print(f"Комментарий: {contact.comment}")
        print('-------------------------------------')

    @staticmethod
    def validate_phone(phone):
        if phone.startswith("+") and phone[1:].isdigit() or phone.isdigit():
            return True
        return False

    @staticmethod
    def ask_to_save_changes(filename):
        while True:
            save_news = input(f'Изменения не сохранены в файл телефонной книги {filename}. Сохранить изменения? y/n ').strip().lower()
            if save_news == 'y':
                return True
            elif save_news == 'n':
                return False
            else:
                print('Введите y/n')
