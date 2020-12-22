from django.dispatch import Signal


post_profile_activate = Signal(providing_args=["profile"])
