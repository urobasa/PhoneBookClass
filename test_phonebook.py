import pytest
import os
import json
from model import Phonebook, Contact, FileHandler

def test_add_contact():
    phonebook = Phonebook()
    contact = Contact(1, "Test Name", "+1234567890", "Test Comment")
    phonebook.add_contact(contact)
    assert len(phonebook.contacts) == 1
    assert phonebook.contacts[0].name == "Test Name"
    _cleanup_file("test_phonebook.json")

def test_search_contacts():
    phonebook = Phonebook()
    contact1 = Contact(1, "Test Name", "+1234567890", "Test Comment")
    contact2 = Contact(2, "Another Name", "+9876543210", "Another Comment")
    contact3 = Contact(1, "Иван Иванов", "+79001112233", "Друг")
    contact4 = Contact(1, "Иван Петров", "+79908769987", "Друг1")
    phonebook.add_contact(contact1)
    phonebook.add_contact(contact2)
    phonebook.add_contact(contact3)
    phonebook.add_contact(contact4)
    assert len(phonebook.search_contacts("Test")) == 1
    assert phonebook.search_contacts("Test")[0].name == "Test Name"
    assert len(phonebook.search_contacts("+9876543210")) == 1
    assert phonebook.search_contacts("+9876543210")[0].phone == "+9876543210"
    assert len(phonebook.search_contacts("Comment")) == 2
    assert len (phonebook.search_contacts("Вася")) == 0
    _cleanup_file("test_phonebook.json")


def test_edit_contact():
    phonebook = Phonebook()
    contact = Contact(1, "Test Name", "+1234567890", "Test Comment")
    phonebook.add_contact(contact)

    phonebook.edit_contact(1, {'name': 'New Name', 'phone': '+0000000000', 'comment': 'New Comment'})

    edited_contact = phonebook.get_contact_by_id(1)
    assert edited_contact.name == "New Name"
    assert edited_contact.phone == "+0000000000"
    assert edited_contact.comment == "New Comment"
    _cleanup_file("test_phonebook.json")

def test_delete_contact():
    phonebook = Phonebook()
    contact = Contact(1, "Test Name", "+1234567890", "Test Comment")
    phonebook.add_contact(contact)
    phonebook.delete_contact(1)
    assert len(phonebook.contacts) == 0
    _cleanup_file("test_phonebook.json")

def test_open_save_file():
    phonebook = Phonebook()
    contact = Contact(1, "Test Name", "+1234567890", "Test Comment")
    phonebook.add_contact(contact)
    test_filename = "test_phonebook.json"

    FileHandler.save_file(test_filename, phonebook.contacts)
    new_phonebook = Phonebook()
    contacts_data = FileHandler.open_file(test_filename)
    new_phonebook.contacts = [Contact.from_dict(c) for c in contacts_data]

    assert len(new_phonebook.contacts) == 1
    assert new_phonebook.contacts[0].name == "Test Name"
    _cleanup_file("test_phonebook.json")


def test_open_new_file():
    contacts_data = FileHandler.open_file("nonexistent_file.json")
    assert contacts_data == []

def test_are_contacts_different():
    phonebook = Phonebook()
    contact = Contact(1, "Test Name", "+1234567890", "Test Comment")
    phonebook.add_contact(contact)
    test_filename = "test_phonebook.json"
    FileHandler.save_file(test_filename, phonebook.contacts)

    assert not FileHandler.are_contacts_different(test_filename, phonebook.contacts)

    contact2 = Contact(2, "Name2", "+1111111111", "Comment2")
    phonebook.add_contact(contact2)
    assert FileHandler.are_contacts_different(test_filename, phonebook.contacts)

    assert FileHandler.are_contacts_different("nonexistent.json", phonebook.contacts)
    _cleanup_file("test_phonebook.json")

def _cleanup_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
