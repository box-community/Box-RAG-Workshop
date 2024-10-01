from typing import List

from box_sdk_gen import BoxClient, File, Folder

from utils.box_client_ccg import AppConfig


def folder_habitat_leases(client: BoxClient, conf: AppConfig) -> Folder:
    items = client.folders.get_folder_items(folder_id=conf.box_root_demo_folder)
    for item in items.entries:
        if item.name == conf.box_folder_leases_name and item.type == "folder":
            return item


def files_start_with(name: str, client: BoxClient, conf: AppConfig) -> List[File]:
    items = client.folders.get_folder_items(
        folder_id=folder_habitat_leases(client, conf).id
    )

    return [
        item
        for item in items.entries
        if item.name.startswith(name) and item.type == "file"
    ]
