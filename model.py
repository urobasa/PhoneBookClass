import json
import os

class Contact:
    def __init__(self, id, name, phone, comment):
        self.id = id
        self.name = name
        self.phone = phone
        self.comment = comment

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'comment': self.comment
        }

    @staticmethod
    def from_dict(data):
        return Contact(data['id'], data['name'], data['phone'], data['comment'])


class Phonebook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def delete_contact(self, contact_id):
        self.contacts = [c for c in self.contacts if c.id != contact_id]

    def edit_contact(self, contact_id, new_data):
        for contact in self.contacts:
            if contact.id == contact_id:
                contact.name = new_data.get('name', contact.name)
                contact.phone = new_data.get('phone', contact.phone)
                contact.comment = new_data.get('comment', contact.comment)
                break

    def search_contacts(self, query):
        return [c for c in self.contacts if query.lower() in c.name.lower() or query.lower() in c.phone.lower() or query.lower() in c.comment.lower()]

    def get_all_contacts(self):
        return self.contacts

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None


class FileHandler:
    @staticmethod
    def are_contacts_different(filename, contacts):
        if not os.path.exists(filename):
            return True
        with open(filename, 'r', encoding='utf-8') as file:
            saved_contacts = json.load(file)
            return saved_contacts != [c.to_dict() for c in contacts]

    @staticmethod
    def open_file(filename):
        contacts = []
        if os.path.exists(filename):
            if os.path.getsize(filename) > 0:
                with open(filename, 'r', encoding='utf-8') as read_fil:
                    contacts = json.load(read_fil)
        return contacts

    @staticmethod
    def save_file(filename, contacts):
        with open(filename, 'w', encoding='utf-8') as file_cre:
            json.dump([c.to_dict() for c in contacts], file_cre, ensure_ascii=False, indent=4)