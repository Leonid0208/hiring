from django import template

register = template.Library()


def htmlattributes(value, arg):
    attrs = value.field.widget.attrs


    data = arg.replace(' ', '')

    kvs = data.split(',')

    for val in kvs:
        kv = val.split(':')
        attrs[kv[0]] = kv[1]
    value.field.widget.attrs = attrs
    rendered = str(value)

    return rendered


register.filter('htmlattributes', htmlattributes)