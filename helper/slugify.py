import re
import random

def slugify(name, chars=50):
    base = name
    base = re.sub(r'[^-.\w\s]', '', base)      
    base = re.sub(r'^[\s.]+|[\s.]+$', '', base)
    base = re.sub(r'[-.\s]+', '-', base)       
    base = base.lower()                        
    slug = base[0:chars]                       
    for i in range(5):
        # Check if the slug already exists in the model
        if slug_already_exists(slug):
            # If it exists, generate a new slug with a random suffix
            slug = "%s-%06x" % (base[0:chars-7], random.randrange(0,0x1000000))
        else:
            return slug


# Mock function to check if slug already exists in the model
def slug_already_exists(slug):
    # Assuming you have some logic here to check if the slug already exists in the model
    # For now, let's just return False
    return False

