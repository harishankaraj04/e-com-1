# 💥 Boom - E-Commerce Platform (Flipkart Style)

An end-to-end, full-featured e-commerce platform built in **Python (Flask)** with a user experience inspired by **Flipkart**.

---

## 🌟 Key Features

1. **Flipkart Look & Feel**:
   - Iconic royal blue header (`#2874f0`) with search bar, user dropdown, Wishlist and Cart counters.
   - Category navigation strip (Mobiles, Laptops, Audio, Appliances, Fashion, Home, Electronics).
   - "Big Boom Days" hero carousel banner.
   - "Deals of the Day" showcase with countdown timer.
   - Flipkart-styled product cards with discount tags, "Boom Assured" badge, ratings pill, and original crossed-out prices.

2. **25 Real-World Products with Images**:
   - Hand-curated catalog of 25 premium items across 7 categories:
     - **Smartphones**: iPhone 15 Pro Max, Galaxy S24 Ultra, OnePlus 12, Pixel 8 Pro, Nothing Phone (2).
     - **Laptops**: MacBook Air M3, ASUS ROG Zephyrus G16, Dell XPS 13 Plus, HP Pavilion 15.
     - **Audio & Wearables**: Sony WH-1000XM5, AirPods Pro 2, Galaxy Watch6 Classic, boAt Airdopes 141.
     - **Home Appliances**: Sony Bravia 55" 4K TV, LG 8kg Steam Washing Machine, Dyson V12 Slim, Philips Air Fryer XL.
     - **Fashion & Lifestyle**: Nike Air Jordan 1s, Levi's 511 Slim Jeans, Ray-Ban Aviators, Fossil Chronograph.
     - **Home & Travel**: Wakefit Orthopedic Mattress, Nespresso Vertuo Pop, Samsonite 75cm Luggage, Kindle Paperwhite.
   - Each item includes high-resolution images, specifications table, key highlights, bank offers, stock levels, and user reviews.
   - Built-in SVG fallback generator so product cards always display seamlessly even offline.

3. **Flipkart Filtering & Sorting**:
   - Search by keyword (product name, brand, category, description).
   - Filter by Category, Price range, Brand, Customer ratings (4★ & above), and Discount percentage.
   - Sort by Popularity, Price (Low to High / High to Low), Discount, and Rating.

4. **Product Detail Page**:
   - Interactive multi-angle image gallery with thumbnail switcher.
   - Flipkart's signature action buttons: Yellow **"ADD TO CART"** and Orange **"BUY NOW"**.
   - Available Bank Offers box with discount tags.
   - Live Delivery Pincode Checker simulation.
   - Full Specifications breakdown and Highlights.
   - Customer Reviews with star distribution progress bars + interactive **"Rate & Review"** modal.

5. **End-to-End Shopping Cart & Checkout**:
   - Cart with quantity stepper (`-`, `qty`, `+`), "Save for later", and "Remove".
   - Sticky "PRICE DETAILS" card with item subtotals, discounts, free delivery threshold, and green savings alert.
   - Multi-step checkout with delivery address form, order summary, and payment choices:
     - **UPI** (Google Pay, PhonePe, Paytm, BHIM)
     - **Credit / Debit / ATM Cards**
     - **Net Banking**
     - **Cash on Delivery (COD)**
   - Order Confirmation page with order tracking progress timeline (`Ordered` -> `Packed` -> `Delivered`), order receipt, and print capability.

6. **Wishlist Management**:
   - Interactive heart button on all cards and product pages.
   - Wishlist page with 1-click "Move to Cart" and delete options.

---

## 🚀 How to Run

1. Open a terminal / command prompt in this directory:
   ```bash
   cd C:\Users\haris\.gemini\antigravity\scratch\boom_ecommerce
   ```

2. (Optional) Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Python Flask application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
