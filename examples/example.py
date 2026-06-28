"""Minimal LabguruPython 2.0 usage example.

Set LABGURU_TOKEN (and optionally LABGURU_URL) in your environment, then run:

    python examples/example.py
"""
import os

from labguru import Labguru


def main():
    lab = Labguru(
        url=os.environ.get("LABGURU_URL", "https://my.labguru.com"),
        token=os.environ["LABGURU_TOKEN"],
    )

    # List the first page of projects (each item is a plain dict).
    for project in lab.projects.list(page=1):
        print(project["id"], project.get("title"))

    # Create a protocol. Arbitrary fields (external_uuid, custom1..N, tags) are
    # passed straight through — useful for keeping cross-system references.
    protocol = lab.protocols.create({
        "name": "My protocol",
        "external_uuid": "external-system-123",
    })
    print("created protocol", protocol["id"])

    # Re-discover an inventory item in a biocollection by its external_uuid.
    plasmids = lab.biocollections.for_collection("plasmids")
    print("matched plasmids:", plasmids.find_by_external_uuid("external-system-123"))

    # Global search across the instance.
    print(lab.search.global_search("My protocol"))


if __name__ == "__main__":
    main()
