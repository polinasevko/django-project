from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TABLE_HEAD = """
    <table class="table table-striped">
        <tbody>
                """

TABLE_TAIL = """
        </tbody>
    </table>
                """

TABLE_CONTENT = """
    <tr>
      <td>{name}</td>
      <td>{value}</td>
    </tr>
"""

PRODUCT_SPECIFICATION = {
    'guitarproduct':
        {
            'Type': 'type',
            'Top material': 'top_material',
            'Nut width': 'nut_width',
            'Frets': 'frets',
        },
    'micproduct':
        {
            'Sensitivity': 'sensitivity',
            'Frequency': ['min_frequency', 'max_frequency'],
        },
    'pianoproduct':
        {
            'Keys': 'keys_number',
            'Weigth': 'weigth',
            'Heigth': 'heigth',
            'Width': 'width',
        },
}


def get_product_specification(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPECIFICATION[model_name].items():
        if isinstance(value, list):
            val = str(getattr(product, value[0])) + ' - ' + str(getattr(product, value[1]))
            table_content += TABLE_CONTENT.format(name=name, value=val)
        else:
            table_content += TABLE_CONTENT.format(name=name, value=str(getattr(product, value)))
    return table_content


@register.filter
def product_specification(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_specification(product, model_name) + TABLE_HEAD)
