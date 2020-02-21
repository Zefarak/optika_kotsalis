from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from catalogue.models import Product
from catalogue.product_attritubes import ProductCharacteristics
from catalogue.product_attritubes import Attribute, AttributeProductClass


@staff_member_required
def copy_product_view(request, pk):
    # instance = get_object_or_404(Product, id=pk)
    old_object = get_object_or_404(Product, id=pk)
    '''
    new_object = Product.objects.create(
        title=instance.title,
        eng_title=instance.eng_title,
        product_class=instance.product_class,
        site_text=instance.site_text,
        eng_site_text=instance.eng_site_text,
        price=instance.price,
        price_discount=instance.price_discount,
        final_price=instance.final_price,
        brand=instance.brand,
        category=instance.category
    )
    '''
    object = get_object_or_404(Product, id=pk)
    object.id = None
    object.qty = 0
    object.slug = None
    object.save()
    object.refresh_from_db()

    for ele in old_object.category_site.all():
        object.category_site.add(ele)
    for ele in old_object.characteristics.all():
        ProductCharacteristics.objects.create(
            product_related=object,
            title=ele.title,
            value=ele.value
        )
    return redirect(object.get_edit_url())
