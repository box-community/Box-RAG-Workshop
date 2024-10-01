from pathlib import Path

from box_sdk_gen import Folder
from tqdm import tqdm

from utils.box_api import file_upload, folder_create
from utils.box_client_ccg import AppConfig, get_ccg_user_client, whoami
from utils.create_samples import execute_mail_merge


def main():
    # execute mail merge
    execute_mail_merge()

    # get box user client
    conf = AppConfig()
    print(f"\nConfiguration:\n{conf.to_dict()}")

    # get ccg user client
    print("\nGetting CCG user client..")
    client = get_ccg_user_client(conf, conf.ccg_user_id)

    # who am i
    user = whoami(client)
    print(f"Who am I: {user.name} (id: {user.id})")

    # create templates folder in box
    print(
        f"\nCreating templates folder in box using parent id {conf.box_root_demo_folder}:"
    )
    templates_folder: Folder = folder_create(
        client=client,
        parent_folder_id=conf.box_root_demo_folder,
        folder_name=conf.box_folder_templates_name,
    )
    # read local template files and upload to box
    print("\nUploading template files:")
    total_bytes = sum(
        f.stat().st_size for f in Path(f"{conf.local_folder_templates}").iterdir()
    )
    progress_bar = tqdm(total=total_bytes, unit="B", unit_scale=True)
    for template_file in Path(f"{conf.local_folder_templates}").iterdir():
        file_upload(
            client=client,
            local_file_path=template_file.as_posix(),
            parent_folder_id=templates_folder.id,
        )
        progress_bar.update(template_file.stat().st_size)
    progress_bar.close()

    # create samples folder in box
    print("\nCreating sample folders:")
    sample_folder: Folder = folder_create(
        client=client,
        parent_folder_id=conf.box_root_demo_folder,
        folder_name=conf.box_folder_leases_name,
    )
    print(f"Sample folder: {sample_folder.id}")

    # read local sample files and upload to box
    print("\nUploading sample files:")
    total_bytes = sum(
        f.stat().st_size for f in Path(f"{conf.local_folder_files}").iterdir()
    )
    progress_bar = tqdm(total=total_bytes, unit="B", unit_scale=True)

    for sample_file in Path(f"{conf.local_folder_files}").iterdir():
        file_upload(
            client=client,
            local_file_path=sample_file.as_posix(),
            parent_folder_id=sample_folder.id,
        )
        progress_bar.update(sample_file.stat().st_size)
    progress_bar.close()
    print()


if __name__ == "__main__":
    main()
