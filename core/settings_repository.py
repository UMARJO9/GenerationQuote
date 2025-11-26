from .settings_loader import load_settings, save_settings


class SettingsRepository:
    def __init__(self, file_path="data/settings.json"):
        self.file_path = file_path
        self.settings = load_settings(file_path)

    # ----- getters -----
    def get_authors(self):
        return list(self.settings.get("authors", []))

    def get_categories(self):
        return list(self.settings.get("categories", []))

    # ----- authors -----
    def add_author(self, name: str):
        name = (name or "").strip()
        if not name:
            return False
        authors = self.settings.setdefault("authors", [])
        if name.lower() in (a.lower() for a in authors):
            return False
        authors.append(name)
        save_settings(self.file_path, self.settings)
        return True

    def delete_author(self, name: str):
        name = (name or "").strip()
        authors = self.settings.setdefault("authors", [])
        before = len(authors)
        authors[:] = [a for a in authors if a.lower() != name.lower()]
        changed = len(authors) != before
        if changed:
            save_settings(self.file_path, self.settings)
        return changed

    # ----- categories -----
    def add_category(self, title: str):
        title = (title or "").strip()
        if not title:
            return False
        categories = self.settings.setdefault("categories", [])
        if title.lower() in (c.lower() for c in categories):
            return False
        categories.append(title)
        save_settings(self.file_path, self.settings)
        return True

    def delete_category(self, title: str):
        title = (title or "").strip()
        categories = self.settings.setdefault("categories", [])
        before = len(categories)
        categories[:] = [c for c in categories if c.lower() != title.lower()]
        changed = len(categories) != before
        if changed:
            save_settings(self.file_path, self.settings)
        return changed

    # ----- reload -----
    def reload(self):
        self.settings = load_settings(self.file_path)
        return self.settings

