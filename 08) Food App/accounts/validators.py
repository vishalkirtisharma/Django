from django.core.exceptions import ValidationError
import os

def allow_only_images_validate(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext.lower() not in valid_extensions:
        print(ValidationError('Unsupported file extension. Allowed extensions: .jpg, .jpeg, .png'))
        raise ValidationError('Unsupported file extension. Allowed extensions: .jpg, .jpeg, .png')