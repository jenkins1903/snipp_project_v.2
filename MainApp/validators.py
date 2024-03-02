from django.core.exceptions import ValidationError

def validate_image_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.jpg', '.png', '.jpeg', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    
def validate_image_size(value):
    limit = 2 * 1024 * 1024  
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MB.')