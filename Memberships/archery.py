from jinja2 import Template

with open('membership_details_template.html', 'r') as file:
    template_string = file.read()

template = Template(template_string)


sport = "Archery"
price = "15.00"


rendered_template = template.render(sport=sport, price=price)


with open('rendered_membership_details.html', 'w') as file:
    file.write(rendered_template)