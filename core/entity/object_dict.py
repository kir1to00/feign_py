class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = ObjectDict(value)
            elif isinstance(value, list):
                self[key] = [ObjectDict(item) if isinstance(item, dict) else item for item in value]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'ObjectDict' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if isinstance(value, dict) and not isinstance(value, ObjectDict):
            value = ObjectDict(value)
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError(f"'ObjectDict' object has no attribute '{name}'")
