from django.db import models
from django.contrib.auth.models import (User,
                                        PermissionsMixin)
# Create your models here.


class User(User, PermissionsMixin):
    """
    Extending the user model
    """
    def __str__(self):
        """
        String representation
        """
        return self.first_name + ' ' + self.last_name
