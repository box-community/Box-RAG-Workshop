from pathlib import Path
from typing import List

import pytest
from box_sdk_gen import (
    BoxClient,
    CreateFolderParent,
    File,
    Folder,
    UploadFileAttributes,
)

from utils.box_client_ccg import (
    AppConfig,
    get_ccg_enterprise_client,
    get_ccg_user_client,
)


@pytest.fixture(scope="module")
def box_env_ccg() -> AppConfig:
    config = AppConfig()
    return config


@pytest.fixture(scope="module")
def box_client_ccg(box_env_ccg: AppConfig) -> BoxClient:
    client = get_ccg_enterprise_client(box_env_ccg)
    return client


@pytest.fixture(scope="module")
def box_client_ccg_user(box_env_ccg: AppConfig) -> BoxClient:
    client = get_ccg_user_client(box_env_ccg, box_env_ccg.ccg_user_id)
    return client


@pytest.fixture(scope="module")
def box_test_samples(box_env_ccg: AppConfig, box_client_ccg_user: BoxClient):
    # create temporary test folder in box
    folder_name = "2024-CCS-Demo-Test-Folder"
    parent = CreateFolderParent(id=box_env_ccg.box_root_demo_folder)
    folder_box: Folder = box_client_ccg_user.folders.create_folder(
        name=folder_name, parent=parent
    )

    # Create a list of Path objects for sample files from reading the samples local folder
    sample_files_local = [
        file_local
        for file_local in Path("src/tests/samples").iterdir()
        if file_local.is_file()
    ]

    # upload local files to box
    sample_files_box: List[File] = []
    sample_files_parent = CreateFolderParent(id=folder_box.id)
    for file_local in sample_files_local:
        attributes = UploadFileAttributes(
            name=file_local.name, parent=sample_files_parent
        )
        with open(file_local, "rb") as file_stream:
            sample_files_box.append(
                box_client_ccg_user.uploads.upload_file(
                    file=file_stream, attributes=attributes
                ).entries[0]
            )

    yield sample_files_box

    # remove test folder
    box_client_ccg_user.folders.delete_folder_by_id(folder_box.id, recursive=True)
