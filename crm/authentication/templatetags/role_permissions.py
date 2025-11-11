from django.template import Library

register = Library()

@register.simple_tag

def display_name(name):

    return name.upper()

@register.simple_tag

def check_roles(request,roles):

    roles =roles.split(',')

    if request.user.is_authenticated and request.user.role in roles:
       
        return True
    
    return False



#    template tag 
#    {% display_name as name %}
#   <p>{{ name }}</p> 

                #    {% display_name 'Adithya' as name %}
                #    <p>{{ name }}</p>