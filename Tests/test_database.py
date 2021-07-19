from unittest import TestCase

from PySide6Extended.core.database import Database


class TestDatabase(TestCase):
    def setUp(self):
        self.db = Database("database", Database.user_folder_path + "/Test/database/")

    def test_set_path(self):
        new_path = "/Test/database1/"
        self.db.set_path(new_path)
        self.assertEqual(self.db.path, new_path)

    def test_set_file_name(self):
        new_name = "file"
        self.db.set_file_name(new_name)
        self.assertEqual(self.db.file_name, new_name)

    def test_create_full_path(self):
        new_path = "/Test/database1/"
        self.db.set_path(new_path)
        new_name = "file"
        self.db.set_file_name(new_name)
        self.db.create_full_path()
        self.assertEqual(self.db.full_path, new_path + new_name)

    def test_save_json(self):
        self.assertTrue(self.db.json_file_exists())

    def test_load_json(self):
        self.db.load_json()
        self.assertEqual(type(self.db.database), dict)
        self.assertDictEqual(self.db.database, {})

    def test_delete_json(self):
        self.db.delete_json()
        self.assertFalse(self.db.json_file_exists())

    def test_table_exists(self):
        self.db.create_table("table")
        self.assertTrue(self.db.table_exists("table"))

    def test_create_table(self):
        self.db.create_table("table")
        self.assertTrue(self.db.table_exists("table"))
        self.assertEqual(self.db.table().__str__(), "{}")

    def test_drop_table(self):
        self.db.create_table("table")
        self.assertTrue(self.db.table_exists("table"))
        self.db.drop_table("table")
        self.assertFalse(self.db.table_exists("table"))

    def test_tables(self):
        self.assertEqual(self.db.tables(), [])
        
    def tearDown(self):
        self.db.delete_json()


class TestTable(TestCase):
    def setUp(self):
        self.db = Database("database", Database.user_folder_path + "/Test/database/")
        self.db.create_table("table")

    def test_insert(self):
        record = {"Name": "Sam"}
        self.db.table().insert(record)
        self.assertEqual(self.db.database["table"]["0"], record)

    def test_insert_many(self):
        records = [{"Name": "Sam"},
                   {"Name": "Anne"},
                   {"Name": "Bran"}]
        self.db.table().insert_many(records)
        self.assertEqual(list(self.db.database["table"].keys()), ["0", "1", "2"])
        self.assertEqual(self.db.database["table"]["0"], records[0])
        self.assertEqual(self.db.database["table"]["1"], records[1])
        self.assertEqual(self.db.database["table"]["2"], records[2])

    def test_delete(self):
        record = {"Name": "Sam"}
        self.db.table().insert(record)
        self.assertEqual(self.db.database["table"]["0"], record)
        self.db.table().delete("0")
        self.assertEqual(self.db.table().records, {})

    def test_delete_many(self):
        records = [{"Name": "Sam"},
                   {"Name": "Anne"},
                   {"Name": "Bran"}]
        self.db.table().insert_many(records)
        self.db.table().delete_many(["0", "1", "2"])
        self.assertEqual(self.db.table().records, {})

    def test_delete_all(self):
        records = [{"Name": "Sam"},
                   {"Name": "Anne"},
                   {"Name": "Bran"}]
        self.db.table().insert_many(records)
        self.db.table().delete_all()
        self.assertEqual(self.db.table().records, {})

    def test_find(self):
        records = [{"Name": "Sam", "Gender": "Male"},
                   {"Name": "Anne", "Gender": "Female"},
                   {"Name": "Bran", "Gender": "Male"}]
        self.db.table().insert_many(records)
        result = self.db.table().find({"Gender": "Male"})
        self.assertEqual(result, [{"Name": "Sam", "Gender": "Male"}, {"Name": "Bran", "Gender": "Male"}])

    def test_find_ids(self):
        records = [{"Name": "Sam", "Gender": "Male"},
                   {"Name": "Anne", "Gender": "Female"},
                   {"Name": "Bran", "Gender": "Male"}]
        self.db.table().insert_many(records)
        result = self.db.table().find_ids({"Gender": "Male"})
        self.assertEqual(result, ["0", "2"])

    def test_update(self):
        records = [{"Name": "Sam", "Gender": "Male"},
                   {"Name": "Anne", "Gender": "Female"},
                   {"Name": "Bran", "Gender": "Male"}]
        self.db.table().insert_many(records)
        self.db.table().update({"Gender": "Male"}, {"Name": "Simon"})
        self.assertEqual(self.db.table().__str__(), "{'0': {'Name': 'Simon', 'Gender': 'Male'}, '1': {'Name': 'Anne', 'Gender': 'Female'}, '2': {'Name': 'Simon', 'Gender': 'Male'}}")

    def test_update_one(self):
        records = [{"Name": "Sam", "Gender": "Male"},
                   {"Name": "Anne", "Gender": "Female"},
                   {"Name": "Bran", "Gender": "Male"}]
        self.db.table().insert_many(records)
        self.db.table().update_one({"Gender": "Male"}, {"Name": "Simon"})
        self.assertEqual(self.db.table().__str__(),
                         "{'0': {'Name': 'Simon', 'Gender': 'Male'}, '1': {'Name': 'Anne', 'Gender': 'Female'}, '2': {'Name': 'Bran', 'Gender': 'Male'}}")

    def tearDown(self):
        self.db.delete_json()
