from django import template


register = template.Library()

@register.filter(name="money_string")
def format_money_like_string(value):
    try:
        total_str, after_comma = str(value).split(".")[0], str(value).split(".")[1]
    except IndexError:
        total_str = str(value)
        after_comma = "00"

    formatted_value = ""
    c = 0
    for i in range(1, len(total_str)+1):
        formatted_value = total_str[-i] + formatted_value 
        c += 1
        if c == 3:
            formatted_value = " " + formatted_value
            c = 0
    formatted_value = formatted_value + "." + after_comma
    return formatted_value 