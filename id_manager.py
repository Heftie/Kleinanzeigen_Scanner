import json
from pathlib import Path

class IDManager:
    def __init__(self, filename="ids.json"):
        self.filename = Path(filename)
        self.data = {"good_ids": [], "filtered_ids": []}
        self._load()

    def _load(self):
        """Load IDs from file if it exists."""
        if self.filename.exists():
            with self.filename.open("r", encoding="utf-8") as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    print("JSON file is corrupted. Starting fresh.")
                    self.data = {"good_ids": [], "filtered_ids": []}

    def save(self):
        """Save IDs to file."""
        with self.filename.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_good(self, offer_id):
        """Add ID to good_ids if not already present."""
        if offer_id not in self.data["good_ids"]:
            self.data["good_ids"].append(offer_id)
            self.save()

    def add_filtered(self, offer_id):
        """Add ID to filtered_ids if not already present."""
        if offer_id not in self.data["filtered_ids"]:
            self.data["filtered_ids"].append(offer_id)
            self.save()

    def exists(self, offer_id):
        """Check if ID exists in either list."""
        return offer_id in self.data["good_ids"] or offer_id in self.data["filtered_ids"]

    def get_all_good(self):
        return self.data["good_ids"]

    def get_all_filtered(self):
        return self.data["filtered_ids"]


# Example usage:
if __name__ == "__main__":
    ids = IDManager()

    # Add IDs
    ids.add_good("12345")
    ids.add_filtered("99999")

    # Check existence
    print(ids.exists("12345"))  # True
    print(ids.exists("88888"))  # False

    # Show lists
    print("Good IDs:", ids.get_all_good())
    print("Filtered IDs:", ids.get_all_filtered())
