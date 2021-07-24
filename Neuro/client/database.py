from PySide6Extended.core.database import Database

# create database and tables

db = Database("neuro_database", Database.user_folder_path + "/Neuro/database/")
db.create_table("Users")
db.create_table("Portals")
db.create_table("Notebooks")


# client management

def get_client(username: str):
    return db.Users().find({"username": username})

def add_client(client_dict: dict):
    db.Users().insert(client_dict)

def update_client(username: str, update_fields: dict):
    db.Users().update({"username": username}, update_fields)

def delete_client(username: str):
    record_id = db.Users().find_ids({"username": username})[0]
    db.Users().delete(record_id)


# portal management

def get_portal(portal_name: str):
    return db.Portals().find({"portal_name": portal_name})

def add_portal(portal_dict):
    db.Portals().insert(portal_dict)

def update_portal(portal_name: str, update_fields: dict):
    db.Portals().update({"portal_name": portal_name}, update_fields)

def delete_portal(portal_name: str):
    record_id = db.Portals().find_ids({"portal_name": portal_name})[0]
    db.Portals().delete(record_id)

# notebook management

def get_all_notebooks():
    return db.Notebooks().records

def get_last_notebook_id():
    id_list = list(db.Notebooks().records.keys())
    if id_list:
        return id_list[-1]
    else:
        return -1

def get_notebook(notebook_id: str):
    return db.Notebooks().find({"id": notebook_id})

def add_notebook(notebook_dict):
    return db.Notebooks().insert(notebook_dict)

def update_notebook(notebook_id: str, update_fields: dict):
    db.Notebooks().update({"id": notebook_id}, update_fields)

def delete_notebook(notebook_id: str):
    record_id = db.Notebooks().find_ids({"id": notebook_id})[0]
    db.Notebooks().delete(record_id)

def get_all_notebook_pages(notebook_id: str):
    if get_notebook(notebook_id):
        return get_notebook(notebook_id)[0]["pages"]
    else:
        return {}

def get_notebook_page(notebook_id: str, page_id: str):
    notebook = get_notebook(notebook_id)[0]
    for page_key in notebook["pages"].keys():
        if notebook["pages"][page_key]["page_id"] == page_id:
            return [page_key, notebook["pages"][page_key]]
    else:
        return []

def add_notebook_page(notebook_id: str, page_dict: dict):
    notebook = get_notebook(notebook_id)
    index = str(int(get_last_notebook_page_id(notebook_id)) + 1)
    notebook["pages"][index] = page_dict
    update_notebook(notebook_id, notebook)

def delete_notebook_page(notebook_id: str, page_id: str):
    notebook = get_notebook(notebook_id)[0]
    for page_key in notebook["pages"].keys():
        if notebook["pages"][page_key]["page_id"] == page_id:
            notebook["pages"].pop(page_key)
            update_notebook(notebook_id, notebook)
            return

def get_last_notebook_page_id(notebook_id: str):
    notebook = get_notebook(notebook_id)
    id_list = list(notebook[0]["pages"].keys())
    if id_list:
        return id_list[-1]
    else:
        return -1