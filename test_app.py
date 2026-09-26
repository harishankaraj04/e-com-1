import unittest
import json
from app import app
from database import init_db

class BoomTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        init_db()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'BOOM', response.data)
        self.assertIn(b'Deals of the Day', response.data)
        self.assertIn(b'Apple iPhone 15 Pro Max', response.data)

    def test_product_detail(self):
        response = self.app.get('/product/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ADD TO CART', response.data)
        self.assertIn(b'BUY NOW', response.data)
        self.assertIn(b'Boom Assured', response.data)

    def test_search_and_filter(self):
        response = self.app.get('/?q=macbook')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MacBook Air M3', response.data)

        # Test category filter
        response = self.app.get('/?category=Fashion')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Air Jordan', response.data)

    def test_cart_api_and_page(self):
        # Add to cart
        res = self.app.post('/api/cart/add', 
                            data=json.dumps({'product_id': 1, 'quantity': 1}), 
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 1)

        # View cart
        res_cart = self.app.get('/cart')
        self.assertEqual(res_cart.status_code, 200)
        self.assertIn(b'PRICE DETAILS', res_cart.data)
        self.assertIn(b'PLACE ORDER', res_cart.data)

    def test_wishlist_api(self):
        res = self.app.post('/api/wishlist/toggle',
                            data=json.dumps({'product_id': 2}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['in_wishlist'])

    def test_checkout_and_order(self):
        # First add an item to cart
        self.app.post('/api/cart/add', 
                      data=json.dumps({'product_id': 10, 'quantity': 1}), 
                      content_type='application/json')
        
        # Checkout GET
        res = self.app.get('/checkout')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'DELIVERY ADDRESS', res.data)
        self.assertIn(b'PAYMENT OPTIONS', res.data)

        # Checkout POST
        post_data = {
            'full_name': 'Haris Test',
            'phone': '9876543210',
            'pincode': '560103',
            'locality': 'Bellandur',
            'address': 'Flat 101, Test Residency',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'payment_method': 'UPI'
        }
        res_post = self.app.post('/checkout', data=post_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn(b'Order Placed Successfully!', res_post.data)
        self.assertIn(b'Estimated Delivery', res_post.data)

    def test_pincode_checker_api(self):
        res = self.app.post('/api/check-pincode',
                            data=json.dumps({'pincode': '560103'}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['valid'])
        self.assertIn('Delivery by', data['delivery_date'])

    def test_add_review_api(self):
        res = self.app.post('/api/review/add',
                            data=json.dumps({
                                'product_id': 1,
                                'user_name': 'Test User',
                                'rating': 5,
                                'title': 'Super phone',
                                'comment': 'Loved the build and display quality!'
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['review']['title'], 'Super phone')

    def test_sorting_endpoints(self):
        for sort_type in ['price_low', 'price_high', 'discount', 'rating', 'newest']:
            res = self.app.get(f'/?sort={sort_type}')
            self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
