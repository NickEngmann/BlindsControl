"""Mock Firebase module for testing."""


class FirebaseApplication:
    """Mock Firebase application."""
    
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.data_store = {}
    
    def get(self, path, name):
        """Mock get method."""
        if path not in self.data_store:
            return None
        if name:
            return self.data_store[path].get(name)
        return self.data_store.get(path, {})
    
    def patch(self, path, data):
        """Mock patch method."""
        if path not in self.data_store:
            self.data_store[path] = {}
        self.data_store[path].update(data)
        return data
    
    def set(self, path, data):
        """Mock set method."""
        self.data_store[path] = data
        return data
    
    def delete(self, path, name):
        """Mock delete method."""
        if path in self.data_store and name in self.data_store[path]:
            del self.data_store[path][name]


def FirebaseApplication(url, auth=None):
    """Factory function for FirebaseApplication."""
    return FirebaseApplication(url, auth)

