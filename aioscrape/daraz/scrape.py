# keys = ['name', 'productUrl', 'originalPrice', 'price', 'discount', 'ratingScore',
#         'review' , 'description', 'brandName', 'sellerName']

keys = ['name']

def get_products(data):
    products = []
    for item in data['mods'].get('listItems', []):
        products.append({
            key: item.get(key, None) for key in keys
        })
    return products