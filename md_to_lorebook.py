import os
import sys
import json

sys.path.append(r"D:\Storage\Source\Python_Modules")
from menelku_utils.utils import timed_cprint


def convert_md_to_json(md_content, uid_counter):
    entries = []
    current_entry = {}

    lines = md_content.split("\n")
    lines_len = len(lines)
    current_line = 0
    for line in lines:
        # A new entry is started when a line starts with #
        # And there is already a filled entry
        if (current_line == lines_len - 1 or line.startswith("#")) and current_entry:
            entries.append(current_entry)
            uid_counter += 1
            current_entry = {}

        # Skip empty lines
        if line == "":
            current_line += 1
            continue

        # Converting header info and creating base entry
        if line.startswith("#"):
            header = line.strip("# ").split(", ")
            current_entry["uid"] = uid_counter
            current_entry["key"] = header
            current_entry["keysecondary"] = []
            current_entry["comment"] = ""
            current_entry["content"] = ""
            current_entry["constant"] = False
            current_entry["selective"] = True
            current_entry["selectiveLogic"] = 0
            current_entry["addMemo"] = True
            current_entry["order"] = 100
            current_entry["position"] = 0
            current_entry["disable"] = False
            current_entry["excludeRecursion"] = False
            current_entry["probability"] = 100
            current_entry["useProbability"] = True
        # Filling entry content
        else:
            current_entry["content"] += line + "\n"

        current_line += 1

    # Adding last entry
    if current_entry:
        entries.append(current_entry)

    return {"entries": entries}, uid_counter


def main():
    folder_path = r"./md_lorebook/"

    if not os.path.isdir(folder_path):
        timed_cprint(
            "This script requires a folder named 'md_lorebook', do not rename or remove it.",
            "red",
        )
        sys.exit(1)

    md_files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(".md"):
                md_path = os.path.join(root, filename)
                md_path = md_path.replace("\\", "/")
                md_files.append(md_path)

    if not md_files:
        timed_cprint("No .md files found in the specified directory.", "red")
        return

    __LOREBOOK_JSON__ = "lorebook.json"
    uid_counter = 0
    entries = []
    for md_path in md_files:
        with open(md_path, "r") as md_file:
            md_content = md_file.read()

        json_content, uid_counter = convert_md_to_json(md_content, uid_counter)
        entries.extend(json_content["entries"])

        timed_cprint(f"Converted {md_path} to lorebook", "green")

    # Envelop entries in a dict, where the key is entry uid
    entries_dict = {}
    for entry in entries:
        entries_dict[entry["uid"]] = entry

    with open(__LOREBOOK_JSON__, "w") as json_file:
        json.dump({"entries": entries_dict}, json_file, indent=2)

    timed_cprint(f"All .md files converted to {__LOREBOOK_JSON__}", "white", "on_green")


if __name__ == "__main__":
    main()
