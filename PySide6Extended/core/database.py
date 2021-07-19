import copy
import os.path
import json


class Database:
    user_folder_path = os.path.expanduser("~")
    default_path = user_folder_path + "/Database/save/"

    def __init__(self, name: str, path: str = None):
        if path is None:
            self.path = Database.default_path
        else:
            self.path = path

        self.file_name = "{}.json".format(name)
        self.full_path = ""
        self.create_full_path()

        self.database = {}
        self.load_json()

    def __str__(self):
        return self.tables().__str__()

    # Table management

    def create_table(self, table_name: str, records: dict = None):
        if self.table_exists(table_name):
            table = Table(table_name, self, self.database[table_name])
        else:
            if records is None:
                table = Table(table_name, self)
            else:
                table = Table(table_name, self, records)
        self.database[table_name] = table.records

        def table_method():
            return table

        table_method.__name__ = table_name
        setattr(self, table_method.__name__, table_method)
        self.save_json()

    def drop_table(self, table: str):
        if self.table_exists(table):
            self.database.pop(table)
            delattr(self, table)
            self.save_json()

    def tables(self):
        tables = list(self.database.keys())
        if not tables:
            return []
        else:
            return tables

    def table_exists(self, table):
        if table in self.database:
            return True
        else:
            return False

    # JSON file management

    def set_path(self, path):
        self.path = path

    def set_file_name(self, name):
        self.file_name = name

    def create_full_path(self):
        self.full_path = os.path.join(self.path, self.file_name)

    def save_json(self):
        with open(self.full_path, "w") as f:
            f.write(json.dumps(self.database, indent=4, sort_keys=True))

    def load_json(self):
        if self.json_file_exists():
            with open(self.full_path, "r") as f:
                self.database = copy.deepcopy(json.loads(f.read()))
                for table in self.tables():
                    self.create_table(table, self.database[table])
        else:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            self.save_json()

    def json_file_exists(self):
        return os.path.exists(self.full_path)

    def delete_json(self):
        if self.json_file_exists():
            os.remove(self.full_path)


class Table:
    def __init__(self, name: str, database: Database, records: dict = None):
        self.name = name
        self.ids = []

        self.database = database
        if records is None:
            self.records = {}
        else:
            self.records = records
            self.ids = list(self.records.keys())

    def __str__(self):
        return self.records.__str__()

    def save(self):
        self.database.database[self.name] = self.records
        self.database.save_json()

    def insert(self, record: dict):
        i = 0
        if self.ids:
            while str(i) in self.ids:
                i += 1
        self.ids.append(str(i))
        self.records[str(i)] = record
        self.ids.sort()
        self.save()
        return i

    def insert_many(self, record_list: list):
        list_of_indexes = []
        for record in record_list:
            list_of_indexes.append(self.insert(record))
        return list_of_indexes

    def delete(self, record_id):
        for record in list(self.records):
            if str(record_id) == record:
                self.records.pop(record)
                self.ids.remove(str(record_id))
        self.save()

    def delete_many(self, record_id_list: list):
        for record_id in record_id_list:
            self.delete(record_id)

    def delete_all(self):
        self.delete_many(list(self.records.keys()))

    def find(self, keys: dict):
        return_list = []
        for record_value in self.records.values():
            for value_key in record_value.keys():
                for search_key in keys.keys():
                    if value_key == search_key:
                        if record_value[value_key] == keys[search_key]:
                            return_list.append(record_value)
        return return_list

    def find_ids(self, keys: dict):
        return_list = []
        for record_key in self.records.keys():
            for value_key in self.records[record_key].keys():
                for search_key in keys.keys():
                    if value_key == search_key:
                        if self.records[record_key][value_key] == keys[search_key]:
                            return_list.append(record_key)
        return return_list

    def update(self, search_keys: dict, replace: dict):
        ids = self.find_ids(search_keys)
        for record_id in ids:
            for key in replace.keys():
                self.records[record_id][key] = replace[key]
        self.save()

    def update_one(self, search_keys: dict, replace: dict):
        ids = self.find_ids(search_keys)
        for record_id in ids[0]:
            for key in replace.keys():
                self.records[record_id][key] = replace[key]
        self.save()
