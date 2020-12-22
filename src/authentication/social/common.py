class SocialBackendBase:
    LABEL = None
    ICON = None

    @classmethod
    def get_icon(cls):
        return cls.ICON

    @classmethod
    def get_label(cls):
        return cls.LABEL
