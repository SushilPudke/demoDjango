from django.dispatch import Signal


post_membership_activate = Signal(providing_args=["user"])
