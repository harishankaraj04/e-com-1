import os
import json
import sqlite3
import random
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = 'boom-ecommerce-secret-key-super-secure-2026'

# Ensure database exists
init_db()

@app.before_request
def setup_session():
    if 'cart' not in session:
        session['cart'] = {}  # {str(product_id): quantity}
    if 'wishlist' not in session:
        session['wishlist'] = []  # [product_id, ...]

@app.context_processor
def inject_global_data():
    cart_count = sum(session.get('cart', {}).values())
    wishlist_count = len(session.get('wishlist', []))
    
    # Pre-fetch categories for the category navigation bar
    categories = [
        {"name": "All", "icon": "bi-grid-fill", "slug": ""},
        {"name": "Mobiles", "icon": "bi-phone", "slug": "Mobiles"},
        {"name": "Laptops", "icon": "bi-laptop", "slug": "Laptops"},
        {"name": "Audio", "icon": "bi-headphones", "slug": "Audio"},
        {"name": "Appliances", "icon": "bi-tv", "slug": "Appliances"},
        {"name": "Fashion", "icon": "bi-handbag", "slug": "Fashion"},
        {"name": "Home", "icon": "bi-house-heart", "slug": "Home"},
        {"name": "Electronics", "icon": "bi-cpu", "slug": "Electronics"}
    ]
    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'categories_list': categories,
        'current_year': datetime.now().year
    }

def format_rupee(amount):
    return f"₹{amount:,}"

def format_number(val):
    try:
        return f"{int(val):,}"
    except (ValueError, TypeError):
        return str(val)

app.jinja_env.filters['rupee'] = format_rupee
app.jinja_env.filters['num'] = format_number

@app.route('/')
def index():
    db = get_db()
    
    # Query parameters
    search_query = request.args.get('q', '').strip()
    selected_category = request.args.get('category', '').strip()
    selected_brand = request.args.get('brand', '').strip()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    min_rating = request.args.get('min_rating', type=float)
    min_discount = request.args.get('min_discount', type=int)
    sort_by = request.args.get('sort', 'popularity')

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search_query:
        query += " AND (title LIKE ? OR brand LIKE ? OR category LIKE ? OR description LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term])

    if selected_category and selected_category.lower() != 'all':
        query += " AND category = ?"
        params.append(selected_category)

    if selected_brand:
        query += " AND brand = ?"
        params.append(selected_brand)

    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)

    if min_discount is not None:
        query += " AND discount_percent >= ?"
        params.append(min_discount)

    # Sorting
    if sort_by == 'price_low':
        query += " ORDER BY price ASC"
    elif sort_by == 'price_high':
        query += " ORDER BY price DESC"
    elif sort_by == 'discount':
        query += " ORDER BY discount_percent DESC"
    elif sort_by == 'rating':
        query += " ORDER BY rating DESC"
    elif sort_by == 'newest':
        query += " ORDER BY id DESC"
    else:  # popularity
        query += " ORDER BY rating_count DESC"

    products_cur = db.execute(query, params).fetchall()
    products = [dict(p) for p in products_cur]

    for p in products:
        p['images'] = json.loads(p['images_json'])
        p['highlights'] = json.loads(p['highlights_json'])
        p['specs'] = json.loads(p['specs_json'])
        p['offers'] = json.loads(p['offers_json'])
        p['in_wishlist'] = p['id'] in session.get('wishlist', [])

    # Get available brands for the filter sidebar
    brands_cur = db.execute("SELECT DISTINCT brand FROM products ORDER BY brand ASC").fetchall()
    brands = [b['brand'] for b in brands_cur]

    # Featured Deals (top discount products)
    deals_cur = db.execute("SELECT * FROM products ORDER BY discount_percent DESC LIMIT 6").fetchall()
    deals = [dict(d) for d in deals_cur]
    for d in deals:
        d['in_wishlist'] = d['id'] in session.get('wishlist', [])

    db.close()
    
    return render_template(
        'index.html',
        products=products,
        deals=deals,
        brands=brands,
        search_query=search_query,
        selected_category=selected_category,
        selected_brand=selected_brand,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        min_discount=min_discount,
        sort_by=sort_by,
        total_results=len(products)
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    db = get_db()
    product_cur = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    
    if not product_cur:
        db.close()
        flash("Product not found.", "danger")
        return redirect(url_for('index'))
    
    product = dict(product_cur)
    product['images'] = json.loads(product['images_json'])
    product['highlights'] = json.loads(product['highlights_json'])
    product['specs'] = json.loads(product['specs_json'])
    product['offers'] = json.loads(product['offers_json'])
    product['in_wishlist'] = product['id'] in session.get('wishlist', [])
    product['in_cart'] = str(product['id']) in session.get('cart', {})

    # Fetch reviews
    reviews_cur = db.execute(
        "SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC", 
        (product_id,)
    ).fetchall()
    reviews = [dict(r) for r in reviews_cur]

    # Similar products in same category
    similar_cur = db.execute(
        "SELECT * FROM products WHERE category = ? AND id != ? LIMIT 4",
        (product['category'], product_id)
    ).fetchall()
    similar_products = [dict(p) for p in similar_cur]
    for sp in similar_products:
        sp['in_wishlist'] = sp['id'] in session.get('wishlist', [])

    # Calculate rating stats
    rating_counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    # Simulate realistic rating distribution for visual bar chart
    total_revs = max(len(reviews), 1)
    for r in reviews:
        score = r.get('rating', 5)
        if score in rating_counts:
            rating_counts[score] += 1
    
    # Delivery date estimate
    est_delivery = (datetime.now() + timedelta(days=2)).strftime("%a, %b %d")

    db.close()

    return render_template(
        'product.html',
        product=product,
        reviews=reviews,
        similar_products=similar_products,
        rating_counts=rating_counts,
        est_delivery=est_delivery
    )

@app.route('/cart')
def cart():
    cart_items_dict = session.get('cart', {})
    cart_products = []
    total_price = 0
    total_original_price = 0

    if cart_items_dict:
        db = get_db()
        ids = list(cart_items_dict.keys())
        placeholders = ','.join('?' for _ in ids)
        query = f"SELECT * FROM products WHERE id IN ({placeholders})"
        cur = db.execute(query, ids).fetchall()
        
        for row in cur:
            p = dict(row)
            p['images'] = json.loads(p['images_json'])
            qty = cart_items_dict[str(p['id'])]
            p['quantity'] = qty
            p['subtotal'] = p['price'] * qty
            p['original_subtotal'] = p['original_price'] * qty
            
            total_price += p['subtotal']
            total_original_price += p['original_subtotal']
            cart_products.append(p)
        db.close()

    total_discount = total_original_price - total_price
    delivery_fee = 0 if total_price >= 500 or total_price == 0 else 40
    final_amount = total_price + delivery_fee

    return render_template(
        'cart.html',
        cart_products=cart_products,
        total_price=total_price,
        total_original_price=total_original_price,
        total_discount=total_discount,
        delivery_fee=delivery_fee,
        final_amount=final_amount
    )

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items_dict = session.get('cart', {})
    if not cart_items_dict:
        flash("Your cart is empty. Add some items to checkout!", "warning")
        return redirect(url_for('index'))

    db = get_db()
    ids = list(cart_items_dict.keys())
    placeholders = ','.join('?' for _ in ids)
    cur = db.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", ids).fetchall()
    
    cart_products = []
    total_price = 0
    total_original_price = 0

    for row in cur:
        p = dict(row)
        p['images'] = json.loads(p['images_json'])
        qty = cart_items_dict[str(p['id'])]
        p['quantity'] = qty
        p['subtotal'] = p['price'] * qty
        p['original_subtotal'] = p['original_price'] * qty
        total_price += p['subtotal']
        total_original_price += p['original_subtotal']
        cart_products.append(p)

    total_discount = total_original_price - total_price
    delivery_fee = 0 if total_price >= 500 else 40
    final_amount = total_price + delivery_fee

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        pincode = request.form.get('pincode', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        payment_method = request.form.get('payment_method', 'UPI')

        if not (full_name and phone and address and pincode and city and state):
            flash("Please fill in all required delivery address fields.", "danger")
            db.close()
            return redirect(url_for('checkout'))

        # Generate unique order id
        order_id = "BM" + datetime.now().strftime("%Y%m%d") + str(random.randint(10000, 99999))
        order_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

        order_items = [{
            "id": p["id"],
            "title": p["title"],
            "price": p["price"],
            "quantity": p["quantity"],
            "image_url": p["image_url"]
        } for p in cart_products]

        db.execute('''
        INSERT INTO orders (
            order_id, full_name, phone, pincode, address, city, state,
            payment_method, total_amount, total_discount, items_json,
            order_date, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id, full_name, phone, pincode, address, city, state,
            payment_method, final_amount, total_discount,
            json.dumps(order_items), order_date, 'Confirmed'
        ))
        db.commit()
        db.close()

        # Clear cart
        session['cart'] = {}
        session.modified = True

        return redirect(url_for('order_success', order_id=order_id))

    db.close()
    return render_template(
        'checkout.html',
        cart_products=cart_products,
        total_price=total_price,
        total_original_price=total_original_price,
        total_discount=total_discount,
        delivery_fee=delivery_fee,
        final_amount=final_amount
    )

@app.route('/order-success/<order_id>')
def order_success(order_id):
    db = get_db()
    order_cur = db.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()
    if not order_cur:
        db.close()
        flash("Order not found.", "danger")
        return redirect(url_for('index'))

    order = dict(order_cur)
    order_items = json.loads(order['items_json'])
    est_delivery = (datetime.now() + timedelta(days=2)).strftime("%A, %d %B %Y")
    db.close()

    return render_template('order_success.html', order=order, order_items=order_items, est_delivery=est_delivery)

@app.route('/wishlist')
def wishlist():
    wishlist_ids = session.get('wishlist', [])
    products = []
    if wishlist_ids:
        db = get_db()
        placeholders = ','.join('?' for _ in wishlist_ids)
        cur = db.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", wishlist_ids).fetchall()
        for row in cur:
            p = dict(row)
            p['images'] = json.loads(p['images_json'])
            p['in_cart'] = str(p['id']) in session.get('cart', {})
            products.append(p)
        db.close()

    return render_template('wishlist.html', products=products)

# API Endpoints for interactive Flipkart experience

@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.get_json() or {}
    product_id = str(data.get('product_id', ''))
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({"success": False, "message": "Product ID required"}), 400

    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    session['cart'] = cart
    session.modified = True

    total_count = sum(cart.values())
    return jsonify({
        "success": True,
        "cart_count": total_count,
        "message": "Item added to cart!"
    })

@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    data = request.get_json() or {}
    product_id = str(data.get('product_id', ''))
    action = data.get('action')  # 'increase', 'decrease', 'remove'

    cart = session.get('cart', {})
    if product_id in cart:
        if action == 'increase':
            cart[product_id] += 1
        elif action == 'decrease':
            cart[product_id] -= 1
            if cart[product_id] <= 0:
                del cart[product_id]
        elif action == 'remove':
            del cart[product_id]

    session['cart'] = cart
    session.modified = True

    # Recalculate totals
    total_count = sum(cart.values())
    return jsonify({
        "success": True,
        "cart_count": total_count,
        "item_qty": cart.get(product_id, 0)
    })

@app.route('/api/wishlist/toggle', methods=['POST'])
def api_wishlist_toggle():
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    if not product_id:
        return jsonify({"success": False, "message": "Invalid Product ID"}), 400

    wishlist = session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        in_wishlist = False
        message = "Removed from Wishlist"
    else:
        wishlist.append(product_id)
        in_wishlist = True
        message = "Added to Wishlist"

    session['wishlist'] = wishlist
    session.modified = True

    return jsonify({
        "success": True,
        "in_wishlist": in_wishlist,
        "wishlist_count": len(wishlist),
        "message": message
    })

@app.route('/api/review/add', methods=['POST'])
def api_add_review():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    user_name = data.get('user_name', 'Verified Buyer').strip()
    rating = int(data.get('rating', 5))
    title = data.get('title', '').strip()
    comment = data.get('comment', '').strip()

    if not (product_id and title and comment):
        return jsonify({"success": False, "message": "Please provide title and comment"}), 400

    db = get_db()
    today_str = datetime.now().strftime("%d %b %Y")
    db.execute('''
    INSERT INTO reviews (product_id, user_name, rating, title, comment, verified, date)
    VALUES (?, ?, ?, ?, ?, 1, ?)
    ''', (product_id, user_name, rating, title, comment, today_str))
    
    # Recalculate average rating
    avg_cur = db.execute("SELECT AVG(rating) as avg_r, COUNT(*) as cnt FROM reviews WHERE product_id = ?", (product_id,)).fetchone()
    new_avg = round(avg_cur['avg_r'], 1) if avg_cur['avg_r'] else rating
    new_cnt = avg_cur['cnt']

    db.execute("UPDATE products SET rating = ?, rating_count = rating_count + 1 WHERE id = ?", (new_avg, product_id))
    db.commit()
    db.close()

    return jsonify({
        "success": True,
        "message": "Review submitted successfully!",
        "new_rating": new_avg,
        "review": {
            "user_name": user_name,
            "rating": rating,
            "title": title,
            "comment": comment,
            "date": today_str
        }
    })

@app.route('/api/check-pincode', methods=['POST'])
def api_check_pincode():
    data = request.get_json() or {}
    pincode = str(data.get('pincode', '')).strip()
    if len(pincode) == 6 and pincode.isdigit():
        est = (datetime.now() + timedelta(days=2)).strftime("%a, %d %b")
        return jsonify({
            "success": True,
            "valid": True,
            "delivery_date": f"Delivery by {est}",
            "is_free": True,
            "message": f"Free Delivery by {est} | Cash on Delivery available"
        })
    else:
        return jsonify({
            "success": False,
            "valid": False,
            "message": "Please enter a valid 6-digit Indian Pincode"
        })

if __name__ == '__main__':
    print("Starting Boom E-Commerce Server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
