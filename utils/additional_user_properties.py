from django.contrib.auth.models import User


@property
def show_name(self):
    if self.first_name:
        return '%s %s' % (self.first_name, self.last_name if self.last_name else '')
    else:
        return self.username


def props_to_user():
    User.add_to_class("show_name", show_name)
