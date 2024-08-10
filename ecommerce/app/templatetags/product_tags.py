from django import template
import math

register = template.Library()


@register.simple_tag
def call_sellprice(price, Discount):
    if Discount is None or Discount is 0:
        return f'{price:,}'

    sellprice = price
    sellprice = math.floor(price - (price * Discount / 100))  # floor is for use integer value

    return f'{sellprice:,}'  # f'{price:,} is for use comma in integer value


@register.simple_tag
def progress_bar(total_quantity, Availability):
    progress_bar = Availability
    progress_bar = math.floor(Availability * (100 / total_quantity))
    return progress_bar

