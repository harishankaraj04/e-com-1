import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'boom_store.db')

PRODUCTS = [
    # 1. Mobiles & Smartphones
    {
        "id": 1,
        "title": "Apple iPhone 15 Pro Max (Natural Titanium, 256 GB)",
        "brand": "Apple",
        "category": "Mobiles",
        "price": 134900,
        "original_price": 159900,
        "discount_percent": 15,
        "rating": 4.7,
        "rating_count": 18452,
        "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 24,
        "description": "iPhone 15 Pro Max forged in aerospace-grade titanium with the groundbreaking A17 Pro chip, a customizable Action button, and the most powerful iPhone camera system ever with 5x optical zoom.",
        "highlights": [
            "256 GB ROM",
            "17.02 cm (6.7 inch) Super Retina XDR OLED Display",
            "48MP + 12MP + 12MP | 12MP Front Camera",
            "A17 Pro Chip, 6 Core Processor with Pro GPU",
            "Titanium Frame with Textured Matte Glass Back",
            "Action button for quick access to favorite features"
        ],
        "specs": {
            "Model Name": "iPhone 15 Pro Max",
            "Color": "Natural Titanium",
            "Display Size": "6.7 inch",
            "Resolution": "2796 x 1290 Pixels",
            "Processor": "A17 Pro Bionic Chip",
            "Internal Storage": "256 GB",
            "Primary Camera": "48MP Main + 12MP Ultra Wide + 12MP 5x Telephoto",
            "Operating System": "iOS 17",
            "Warranty": "1 Year Brand Warranty"
        },
        "offers": [
            "Bank Offer: 10% Instant Discount on HDFC Bank Credit Cards, up to ₹4,000",
            "Special Price: Get extra ₹25,000 off (price inclusive of cashback/coupon)",
            "No Cost EMI available starting from ₹11,241/month",
            "Partner Offer: Free 6-Month Boom Plus Membership"
        ]
    },
    {
        "id": 2,
        "title": "Samsung Galaxy S24 Ultra 5G (Titanium Black, 512 GB)",
        "brand": "Samsung",
        "category": "Mobiles",
        "price": 129999,
        "original_price": 144999,
        "discount_percent": 10,
        "rating": 4.6,
        "rating_count": 9320,
        "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 18,
        "description": "Welcome to the era of mobile AI. With Galaxy S24 Ultra in your hands, you can unleash whole new levels of creativity, productivity and possibility starting with the most important device in your life.",
        "highlights": [
            "12 GB RAM | 512 GB ROM",
            "17.27 cm (6.8 inch) Quad HD+ Dynamic AMOLED 2X Display",
            "200MP + 50MP + 12MP + 10MP | 12MP Front Camera",
            "5000 mAh Lithium-ion Battery with 45W Fast Charging",
            "Snapdragon 8 Gen 3 Processor",
            "Built-in S-Pen with Air Commands"
        ],
        "specs": {
            "Model Name": "Galaxy S24 Ultra 5G",
            "Color": "Titanium Black",
            "Display Size": "6.8 inch",
            "Resolution": "3120 x 1440 Pixels",
            "Processor": "Snapdragon 8 Gen 3 for Galaxy",
            "RAM": "12 GB",
            "Internal Storage": "512 GB",
            "Primary Camera": "200MP OIS Quad Camera",
            "Operating System": "Android 14 with One UI 6.1"
        },
        "offers": [
            "Bank Offer: Flat ₹6,000 Instant Discount on ICICI Bank Cards",
            "Exchange Offer: Up to ₹35,000 off on exchange of your old smartphone",
            "No Cost EMI from ₹10,833/month"
        ]
    },
    {
        "id": 3,
        "title": "OnePlus 12 5G (Silky Black, 16GB RAM, 512GB)",
        "brand": "OnePlus",
        "category": "Mobiles",
        "price": 64999,
        "original_price": 69999,
        "discount_percent": 7,
        "rating": 4.5,
        "rating_count": 8110,
        "image_url": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 35,
        "description": "OnePlus 12 defines peak performance with the Snapdragon 8 Gen 3 processor, 4th Gen Hasselblad Camera system, and ultra-fast 100W SUPERVOOC flash charging.",
        "highlights": [
            "16 GB RAM | 512 GB ROM",
            "17.32 cm (6.82 inch) 2K 120Hz ProXDR Display",
            "50MP (Sony LYT-808) + 64MP + 48MP | 32MP Front Camera",
            "5400 mAh Battery with 100W SuperVOOC & 50W AIRVOOC Wireless",
            "Hasselblad Camera for Mobile"
        ],
        "specs": {
            "Model Name": "OnePlus 12",
            "Color": "Silky Black",
            "Processor": "Snapdragon 8 Gen 3",
            "RAM": "16 GB",
            "Storage": "512 GB",
            "Battery": "5400 mAh",
            "Operating System": "OxygenOS based on Android 14"
        },
        "offers": [
            "Bank Offer: ₹3,000 Instant Discount with Axis Bank Cards",
            "Free OnePlus Wireless Bullet Earphones on prepaid orders"
        ]
    },
    {
        "id": 4,
        "title": "Google Pixel 8 Pro (Bay Blue, 128 GB)",
        "brand": "Google",
        "category": "Mobiles",
        "price": 89999,
        "original_price": 106999,
        "discount_percent": 15,
        "rating": 4.4,
        "rating_count": 5214,
        "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 15,
        "description": "Meet Pixel 8 Pro, the all-pro phone engineered by Google. Powered by Google Tensor G3, it has incredible AI capabilities, next-level photography, and 7 years of software updates.",
        "highlights": [
            "12 GB RAM | 128 GB ROM",
            "17.02 cm (6.7 inch) Super Actua OLED Display",
            "50MP + 48MP + 48MP | 10.5MP Front Camera",
            "Google Tensor G3 Processor with Titan M2 security",
            "Best Take and Magic Audio Eraser AI Features"
        ],
        "specs": {
            "Model Name": "Pixel 8 Pro",
            "Color": "Bay Blue",
            "Display Size": "6.7 inch 120Hz LTPO",
            "Processor": "Google Tensor G3",
            "Battery": "5050 mAh",
            "OS": "Pure Android 14"
        },
        "offers": [
            "Flat ₹8,000 Cashback on SBI Credit Cards",
            "7 Days Replacement Guarantee"
        ]
    },
    {
        "id": 5,
        "title": "Nothing Phone (2) (Dark Grey, 128 GB, 8GB RAM)",
        "brand": "Nothing",
        "category": "Mobiles",
        "price": 36999,
        "original_price": 44999,
        "discount_percent": 17,
        "rating": 4.4,
        "rating_count": 14210,
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02596?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02596?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 42,
        "description": "Come to the bright side. Phone (2) features the iconic Glyph Interface, Snapdragon 8+ Gen 1 flagship chipset, dual 50MP Sony sensors, and clean Nothing OS 2.5.",
        "highlights": [
            "8 GB RAM | 128 GB ROM",
            "17.02 cm (6.7 inch) Flexible OLED Display (1-120 Hz)",
            "50MP (Sony IMX890 OIS) + 50MP Ultra Wide | 32MP Front",
            "Qualcomm Snapdragon 8+ Gen 1 Processor",
            "Unique Transparent Glyph Interface with 33 zones"
        ],
        "specs": {
            "Model": "Phone (2)",
            "Color": "Dark Grey",
            "Processor": "Snapdragon 8+ Gen 1",
            "Battery": "4700 mAh",
            "Charging": "45W Fast Charging + 15W Wireless"
        },
        "offers": [
            "Special Price: Extra ₹8,000 off during Boom Sale",
            "Free Case & Screen Protector inside the box"
        ]
    },

    # 2. Laptops & Computers
    {
        "id": 6,
        "title": "Apple MacBook Air M3 (13.6-inch, 16GB Unified RAM, 512GB SSD)",
        "brand": "Apple",
        "category": "Laptops",
        "price": 114900,
        "original_price": 134900,
        "discount_percent": 14,
        "rating": 4.8,
        "rating_count": 4820,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 20,
        "description": "Supercharged by the M3 chip, the strikingly thin MacBook Air blazes through work and play. Up to 18 hours of battery life and support for up to two external displays.",
        "highlights": [
            "Apple M3 Chip (8-Core CPU, 10-Core GPU)",
            "16 GB Unified Memory | 512 GB SSD",
            "34.54 cm (13.6 inch) Liquid Retina Display with True Tone",
            "Backlit Magic Keyboard with Touch ID",
            "Up to 18 Hours Battery Life | MagSafe 3 Charging"
        ],
        "specs": {
            "Processor": "Apple M3 Chip",
            "RAM": "16 GB Unified Memory",
            "Storage": "512 GB SSD",
            "Display": "13.6 inch Liquid Retina (2560 x 1664)",
            "Weight": "1.24 kg",
            "Operating System": "macOS Sonoma"
        },
        "offers": [
            "Bank Offer: ₹5,000 Instant Discount on HDFC Cards",
            "No Cost EMI from ₹9,575/month"
        ]
    },
    {
        "id": 7,
        "title": "ASUS ROG Zephyrus G16 Gaming Laptop (Intel Core Ultra 9, RTX 4070, 32GB, 1TB)",
        "brand": "ASUS",
        "category": "Laptops",
        "price": 179990,
        "original_price": 215990,
        "discount_percent": 16,
        "rating": 4.7,
        "rating_count": 1490,
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 12,
        "description": "Precision gaming meets ultra-sleek design. ROG Zephyrus G16 features a stunning 2.5K 240Hz OLED ROG Nebula display, Intel Core Ultra 9 185H processor, and NVIDIA GeForce RTX 4070 Laptop GPU.",
        "highlights": [
            "Intel Core Ultra 9 185H (16 Cores, 22 Threads)",
            "32 GB LPDDR5X RAM | 1 TB PCIe 4.0 NVMe SSD",
            "8 GB NVIDIA GeForce RTX 4070 GDDR6 Graphics",
            "40.64 cm (16 inch) 2.5K OLED 240Hz 0.2ms Display",
            "Slash Lighting Array on Aluminum CNC Chassis"
        ],
        "specs": {
            "Processor": "Intel Core Ultra 9 185H",
            "Graphics": "NVIDIA GeForce RTX 4070 (8GB)",
            "RAM": "32 GB LPDDR5X",
            "Storage": "1 TB SSD",
            "Refresh Rate": "240 Hz",
            "Weight": "1.85 kg"
        },
        "offers": [
            "Free Xbox Game Pass for 3 Months",
            "Exchange bonus up to ₹20,000"
        ]
    },
    {
        "id": 8,
        "title": "Dell XPS 13 Plus (Core i7 13th Gen, 16GB, 1TB SSD, 3.5K OLED Touch)",
        "brand": "Dell",
        "category": "Laptops",
        "price": 142990,
        "original_price": 168990,
        "discount_percent": 15,
        "rating": 4.5,
        "rating_count": 2100,
        "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 14,
        "description": "The Dell XPS 13 Plus is twice as powerful as before, with a seamless glass touchpad, capacitive touch function row, edge-to-edge zero-lattice keyboard, and vivid 3.5K OLED touch screen.",
        "highlights": [
            "13th Gen Intel Core i7-1360P (12 Cores, 5.0 GHz Turbo)",
            "16 GB LPDDR5 RAM | 1 TB M.2 PCIe Gen 4 SSD",
            "34.03 cm (13.4 inch) 3.5K (3456x2160) OLED InfinityEdge Touch",
            "Seamless Glass Touchpad with Haptics",
            "CNC Machined Aluminum chassis (1.23 kg)"
        ],
        "specs": {
            "Processor": "13th Gen Intel Core i7",
            "Screen": "13.4-inch 3.5K OLED Touch",
            "RAM": "16 GB",
            "Storage": "1 TB SSD",
            "OS": "Windows 11 Home + MS Office 2021"
        },
        "offers": [
            "Bank Offer: 10% off on SBI Credit Cards",
            "Free Dell Premier Wireless Mouse & Sleeve"
        ]
    },
    {
        "id": 9,
        "title": "HP Pavilion 15 (AMD Ryzen 7 7730U, 16GB RAM, 1TB SSD, FHD IPS)",
        "brand": "HP",
        "category": "Laptops",
        "price": 62490,
        "original_price": 76990,
        "discount_percent": 18,
        "rating": 4.3,
        "rating_count": 8940,
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 30,
        "description": "Stay productive and entertained with the HP Pavilion 15. Powered by AMD Ryzen 7, featuring audio by B&O, micro-edge anti-glare display, and fast charging technology.",
        "highlights": [
            "AMD Ryzen 7 7730U (8 Cores, 16 Threads, up to 4.5 GHz)",
            "16 GB DDR4 RAM | 1 TB PCIe NVMe SSD",
            "39.6 cm (15.6 inch) Full HD IPS Micro-Edge Display",
            "Audio by Bang & Olufsen (B&O)",
            "HP Fast Charge: 50% in 45 minutes"
        ],
        "specs": {
            "Processor": "AMD Ryzen 7 7730U",
            "RAM": "16 GB DDR4",
            "Storage": "1 TB SSD",
            "Display": "15.6 inch FHD (1920 x 1080)",
            "OS": "Windows 11 Home"
        },
        "offers": [
            "Extra ₹1,500 off on UPI transactions",
            "1 Year Onsite Manufacturer Warranty"
        ]
    },

    # 3. Audio & Wearables
    {
        "id": 10,
        "title": "Sony WH-1000XM5 Wireless Active Noise Cancelling Headphones",
        "brand": "Sony",
        "category": "Audio",
        "price": 26990,
        "original_price": 34990,
        "discount_percent": 22,
        "rating": 4.6,
        "rating_count": 12850,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 45,
        "description": "With two processors and 8 microphones, Sony WH-1000XM5 wireless noise cancelling headphones rewrite the rules for distraction-free listening and exceptional call quality with Auto NC Optimizer.",
        "highlights": [
            "Industry Leading Active Noise Cancellation with Auto NC Optimizer",
            "Up to 30 Hours Battery Life with Quick Charge (3 min = 3 hrs)",
            "Multipoint connection: Seamlessly switch between 2 devices",
            "Speak-to-chat and Quick Attention mode",
            "Ultra-comfortable lightweight leather fit"
        ],
        "specs": {
            "Type": "Over-Ear Wireless Headphone",
            "Battery Life": "30 Hours ANC On, 40 Hours ANC Off",
            "Bluetooth": "Version 5.2 (LDAC, AAC, SBC)",
            "Weight": "250 grams",
            "Driver Unit": "30mm precision engineered"
        },
        "offers": [
            "Bank Offer: ₹2,000 Instant Discount with Axis Bank Cards",
            "No Cost EMI available"
        ]
    },
    {
        "id": 11,
        "title": "Apple AirPods Pro (2nd Generation with MagSafe Case USB-C)",
        "brand": "Apple",
        "category": "Audio",
        "price": 20999,
        "original_price": 24900,
        "discount_percent": 15,
        "rating": 4.7,
        "rating_count": 31200,
        "image_url": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 50,
        "description": "AirPods Pro feature up to 2x more Active Noise Cancellation, Adaptive Audio, Transparency mode, and Personalized Spatial Audio with dynamic head tracking for immersive sound.",
        "highlights": [
            "Apple H2 Headphone Chip and U1/H2 MagSafe Case Chip",
            "Up to 2x Active Noise Cancellation compared to Gen 1",
            "Adaptive Audio and Conversation Awareness",
            "Up to 30 Hours Total Listening Time with MagSafe Case",
            "Dust, sweat, and water resistant (IP54)"
        ],
        "specs": {
            "Connectivity": "Bluetooth 5.3",
            "Charging Port": "USB-C & MagSafe Wireless",
            "Battery": "6 hours on single charge, 30 hours with case",
            "Sensors": "Skin-detect, motion accelerometer, speech accelerometer"
        },
        "offers": [
            "Flat ₹1,500 off on HDFC & SBI Bank Cards",
            "Free Apple Music trial for 6 months"
        ]
    },
    {
        "id": 12,
        "title": "Samsung Galaxy Watch6 Classic LTE (47mm, Black Sapphire Glass)",
        "brand": "Samsung",
        "category": "Audio",
        "price": 32999,
        "original_price": 42999,
        "discount_percent": 23,
        "rating": 4.5,
        "rating_count": 3410,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 22,
        "description": "The timeless heritage look of Galaxy Watch6 Classic comes alive with a rotating physical bezel, Sapphire Crystal Super AMOLED display, advanced sleep coaching, and ECG blood pressure monitoring.",
        "highlights": [
            "1.5 inch (37.3mm) Super AMOLED Always-on Sapphire Display",
            "Iconic Physical Rotating Bezel for smooth navigation",
            "Advanced Sleep Coaching with snoring and SpO2 tracking",
            "BioActive Sensor: ECG, Blood Pressure, Body Composition (BIA)",
            "Standalone 4G LTE Connectivity (eSIM support)"
        ],
        "specs": {
            "Case Size": "47 mm Stainless Steel",
            "Operating System": "Wear OS powered by Samsung",
            "Battery": "425 mAh with Fast Wireless Charging",
            "Water Resistance": "5ATM + IP68 / MIL-STD-810H"
        },
        "offers": [
            "Bank Offer: ₹3,000 instant discount on ICICI cards",
            "Boom Assured Free Express Delivery"
        ]
    },
    {
        "id": 13,
        "title": "boAt Airdopes 141 Bluetooth True Wireless Earbuds (42H Playtime)",
        "brand": "boAt",
        "category": "Audio",
        "price": 1299,
        "original_price": 4490,
        "discount_percent": 71,
        "rating": 4.1,
        "rating_count": 189200,
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 120,
        "description": "Experience non-stop grooving with boAt Airdopes 141. Armed with 8mm drivers, BEAST Mode 80ms low latency for gaming, ENx environmental noise cancellation for calls, and ASAP Charge.",
        "highlights": [
            "Up to 42 Hours of Total Playback",
            "ASAP Fast Charge: 5 minutes charge gives 75 minutes playtime",
            "BEAST Mode Low Latency for Mobile Gaming",
            "ENx Technology for crystal-clear voice calls",
            "IPX4 Water and Sweat Resistance"
        ],
        "specs": {
            "Driver Size": "8 mm Bass Drivers",
            "Bluetooth": "Version 5.1",
            "Charging Interface": "Type-C",
            "Playback": "42 Hours total"
        },
        "offers": [
            "Special Price: Flat 71% off during Mega Boom Sale",
            "Buy 2 get additional 5% off"
        ]
    },

    # 4. TV & Home Appliances
    {
        "id": 14,
        "title": "Sony Bravia 55 inch 4K Ultra HD Smart Google TV (KD-55X74L)",
        "brand": "Sony",
        "category": "Appliances",
        "price": 57990,
        "original_price": 99900,
        "discount_percent": 41,
        "rating": 4.6,
        "rating_count": 14200,
        "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 16,
        "description": "Sony Bravia 55X74L delivers vibrant real-world colors powered by the X1 4K Processor. Includes Live Colour, 4K X-Reality PRO upscaling, and Dolby Audio with open baffle stereo speakers.",
        "highlights": [
            "4K Ultra HD (3840 x 2160 Pixels) | 60 Hz Refresh Rate",
            "20 Watts Sound Output with Dolby Audio & Open Baffle Speakers",
            "Google TV with Google Assistant & Chromecast built-in",
            "X1 4K Processor with Motionflow XR 100",
            "3 HDMI ports (eARC) & 2 USB ports"
        ],
        "specs": {
            "Screen Size": "55 inch (138.8 cm)",
            "Resolution": "4K Ultra HD (3840 x 2160)",
            "Smart OS": "Google TV",
            "Sound Output": "20 W Dolby Audio",
            "Warranty": "1 Year Comprehensive + 1 Year additional on Panel"
        },
        "offers": [
            "Bank Offer: ₹4,000 instant discount on SBI & Axis Bank Credit Cards",
            "Free Wall-mount Installation within 48 hours"
        ]
    },
    {
        "id": 15,
        "title": "LG 8 kg 5 Star AI Direct Drive Front Load Washing Machine",
        "brand": "LG",
        "category": "Appliances",
        "price": 34990,
        "original_price": 47990,
        "discount_percent": 27,
        "rating": 4.4,
        "rating_count": 6800,
        "image_url": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 10,
        "description": "LG AI Direct Drive front loader automatically detects fabric weight and softness to provide optimal wash motion. Steam hygiene wash eliminates 99.9% of bacteria and allergens.",
        "highlights": [
            "Capacity: 8 kg, suitable for large families (5+ members)",
            "Energy Rating: 5 Star Best in Class Energy Efficiency",
            "AI DD (Artificial Intelligence Direct Drive) 6 Motion Technology",
            "Steam Wash removes 99.9% allergens with baby care program",
            "10-Year Warranty on Inverter Direct Drive Motor"
        ],
        "specs": {
            "Capacity": "8 kg",
            "Max Spin Speed": "1400 RPM",
            "Energy Rating": "5 Star",
            "Tub Material": "Full Stainless Steel",
            "Warranty": "2 Years comprehensive, 10 Years on Motor"
        },
        "offers": [
            "Exchange bonus: Up to ₹4,500 off on old washing machine",
            "Boom Assured Free scheduled delivery and setup"
        ]
    },
    {
        "id": 16,
        "title": "Dyson V12 Detect Slim Wireless Cordless Vacuum Cleaner",
        "brand": "Dyson",
        "category": "Appliances",
        "price": 44900,
        "original_price": 55900,
        "discount_percent": 19,
        "rating": 4.8,
        "rating_count": 3120,
        "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 15,
        "description": "Dyson's most lightweight intelligent cordless vacuum cleaner. Laser illumination reveals microscopic dust on hard floors. Piezo sensor continuously sizes and counts dust particles.",
        "highlights": [
            "Laser reveals microscopic invisible dust particles",
            "Powerful Dyson Hyperdymium motor spins up to 125,000 RPM",
            "Up to 60 Minutes of fade-free run time",
            "LCD screen displays scientific proof of a deep clean in real time",
            "Hair screw tool cleans long hair and pet hair without tangles"
        ],
        "specs": {
            "Suction Power": "150 Air Watts",
            "Weight": "2.2 kg Lightweight",
            "Bin Capacity": "0.35 Litres",
            "Charge Time": "4 Hours",
            "Warranty": "2 Years Dyson India Warranty"
        },
        "offers": [
            "Bank Offer: ₹3,000 off on HDFC & ICICI Bank Cards",
            "Includes 5 additional cleaning attachments"
        ]
    },
    {
        "id": 17,
        "title": "Philips Digital Air Fryer XL (6.2L Capacity, Connected Rapid Air)",
        "brand": "Philips",
        "category": "Appliances",
        "price": 8999,
        "original_price": 14995,
        "discount_percent": 40,
        "rating": 4.5,
        "rating_count": 16400,
        "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 38,
        "description": "Cook healthy and delicious fried dishes with up to 90% less fat. Rapid Air Technology swirls hot air to create crispy outside and tender inside dishes with little to no added oil.",
        "highlights": [
            "6.2 Litre XL Pan capacity cooks up to 5 meal portions at once",
            "Rapid Air Technology with unique starfish bottom design",
            "Touch screen with 7 presets: frozen snacks, fries, meat, fish, baking",
            "Keep warm function keeps food at ideal temperature for 30 mins",
            "Dishwasher safe non-stick basket"
        ],
        "specs": {
            "Power": "2000 Watts",
            "Capacity": "6.2 L / 1.2 kg",
            "Color": "Deep Black & Silver",
            "Warranty": "2 Years Worldwide Guarantee"
        },
        "offers": [
            "Extra ₹500 off using coupon BOOM500",
            "Free NutriU recipe booklet included"
        ]
    },

    # 5. Fashion & Footwear
    {
        "id": 18,
        "title": "Nike Air Jordan 1 Retro High OG Men's Sneakers",
        "brand": "Nike",
        "category": "Fashion",
        "price": 16995,
        "original_price": 19995,
        "discount_percent": 15,
        "rating": 4.8,
        "rating_count": 5890,
        "image_url": "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 16,
        "description": "The sneaker that started it all. The Air Jordan 1 Retro High OG delivers legendary style and premium comfort with genuine full-grain leather and encapsulated Nike Air-Sole cushioning.",
        "highlights": [
            "Genuine leather upper provides durability and structured support",
            "Encapsulated Air-Sole unit in the heel for lightweight cushioning",
            "Solid rubber outsole with deep flex grooves for traction",
            "Iconic Wings logo stamped on the collar",
            "Classic Chicago inspired colorway"
        ],
        "specs": {
            "Style Code": "DZ5485-612",
            "Upper Material": "100% Genuine Leather",
            "Sole": "Rubber Cupsole",
            "Closure": "Lace-Up",
            "Ideal For": "Men / Unisex Sneakerheads"
        },
        "offers": [
            "Boom Assured: 100% Authenticity Verified Guarantee",
            "Free 10-day exchange for sizing"
        ]
    },
    {
        "id": 19,
        "title": "Levi's Men's 511 Slim Fit Stretch Denim Jeans",
        "brand": "Levi's",
        "category": "Fashion",
        "price": 2399,
        "original_price": 3999,
        "discount_percent": 40,
        "rating": 4.3,
        "rating_count": 24800,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 65,
        "description": "A modern slim with room to move. Levi's 511 Slim Fit Jeans are a classic since right now. Cut close through the thigh with a slim leg for an authentic, streamlined aesthetic.",
        "highlights": [
            "Slim from hip to ankle with modern tapered silhouette",
            "99% Cotton, 1% Elastane for built-in stretch and all-day comfort",
            "Signature Arcuate stitching on back pockets",
            "Zip fly with heavy-duty metal button closure",
            "Water<Less technology made with 96% recycled water"
        ],
        "specs": {
            "Fit": "Slim Fit",
            "Fabric": "Cotton Blend Denim",
            "Wash Care": "Machine Wash Cold Inside Out",
            "Rise": "Mid Rise"
        },
        "offers": [
            "Buy 2 get additional 10% off automatically at checkout",
            "Available in multiple waist sizes (28 - 38)"
        ]
    },
    {
        "id": 20,
        "title": "Ray-Ban Classic Polarized Aviator Sunglasses (Gold/Green G-15)",
        "brand": "Ray-Ban",
        "category": "Fashion",
        "price": 8490,
        "original_price": 11990,
        "discount_percent": 29,
        "rating": 4.7,
        "rating_count": 7820,
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 25,
        "description": "Originally designed for U.S. aviators in 1937, Ray-Ban Aviator Classic sunglasses combine great aviator styling with exceptional quality, performance and comfort with polarized crystal lenses.",
        "highlights": [
            "Polarized green classic G-15 lenses block 99% of reflected glare",
            "100% UV400 Protection against harmful UVA and UVB rays",
            "Durable gold-toned lightweight metal frame",
            "Adjustable silicone nose pads for custom comfort",
            "Includes official Ray-Ban protective leather case & microfiber cloth"
        ],
        "specs": {
            "Model Code": "RB3025 001/58",
            "Frame Material": "Metal",
            "Lens Type": "Polarized Mineral Glass",
            "Frame Size": "58 mm Standard",
            "Warranty": "2 Years International Warranty"
        },
        "offers": [
            "Special Price: Extra ₹1,000 off on prepaid orders",
            "100% Original Brand Assured"
        ]
    },
    {
        "id": 21,
        "title": "Fossil Gen 6 Men's Chronograph Stainless Steel & Leather Watch",
        "brand": "Fossil",
        "category": "Fashion",
        "price": 11495,
        "original_price": 18495,
        "discount_percent": 37,
        "rating": 4.4,
        "rating_count": 4910,
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 28,
        "description": "Inspired by American vintage style, this Fossil timepiece features a deep navy blue sunray dial, tachymeter bezel, 3-hand quartz chronograph movement, and rich saddle brown leather strap.",
        "highlights": [
            "44 mm Stainless Steel case with scratch-resistant mineral crystal",
            "Chronograph stopwatch movement with 24-hour sub-dial and date window",
            "Genuine supple 22mm interchangeable leather strap",
            "Water resistant up to 50 meters (5 ATM)",
            "Presented in an authentic collectible Fossil vintage tin box"
        ],
        "specs": {
            "Case Diameter": "44 mm",
            "Case Thickness": "11 mm",
            "Strap Width": "22 mm",
            "Movement": "Quartz Chronograph",
            "Warranty": "2 Years Domestic Warranty"
        },
        "offers": [
            "Bank Offer: 10% instant off on Axis Bank credit cards",
            "Free gift packaging available at checkout"
        ]
    },

    # 6. Home & Lifestyle / Gadgets
    {
        "id": 22,
        "title": "Wakefit Orthopedic Memory Foam Mattress (King Size, 78x72x8 inch)",
        "brand": "Wakefit",
        "category": "Home",
        "price": 12499,
        "original_price": 18999,
        "discount_percent": 34,
        "rating": 4.6,
        "rating_count": 42100,
        "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 20,
        "description": "Engineered for optimal spinal alignment and pressure relief. Features differential zoned support, breathable next-gen memory foam, and high resiliency transition foam.",
        "highlights": [
            "Dimensions: 78 x 72 x 8 inches (King Size)",
            "High Density Next-Gen Memory Foam adapts to your posture",
            "Differential Zoned Support for back pain relief",
            "Breathable premium quilted zipper outer cover (washable)",
            "100 Nights Free Sleep Trial with 10 Years Warranty"
        ],
        "specs": {
            "Mattress Type": "Orthopedic Memory Foam",
            "Firmness": "Medium Firm (Ideal for back support)",
            "Warranty": "10 Years Manufacturer Warranty",
            "Trial Period": "100 Nights Risk Free"
        },
        "offers": [
            "Free 2 Memory Foam Pillows worth ₹1,999",
            "Doorstep unboxing and setup included"
        ]
    },
    {
        "id": 23,
        "title": "Nespresso Vertuo Pop Automatic Espresso & Coffee Machine",
        "brand": "Nespresso",
        "category": "Home",
        "price": 14999,
        "original_price": 19999,
        "discount_percent": 25,
        "rating": 4.5,
        "rating_count": 3290,
        "image_url": "https://images.unsplash.com/photo-1517668808822-9ebd02f2a8ea?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1517668808822-9ebd02f2a8ea?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 18,
        "description": "Bring cafe quality coffee into your kitchen with Nespresso Vertuo Pop. Utilizes Centrifusion technology to read barcodes on capsules and brew espresso, double espresso, gran lungo, or large mug with silky crema.",
        "highlights": [
            "Brews 4 cup sizes: Espresso (40ml), Double Espresso (80ml), Gran Lungo (150ml), Mug (230ml)",
            "Centrifusion Extraction Technology spins capsule at 4000 RPM",
            "Single-button intuitive operation with 30-second rapid heat-up",
            "Compact footprint fits seamlessly on any kitchen countertop",
            "Includes welcome set of 12 assorted coffee capsules"
        ],
        "specs": {
            "Water Tank": "0.6 Litres Removable",
            "Color": "Licorice Black",
            "Power": "1260 Watts",
            "Warranty": "2 Years Official Warranty"
        },
        "offers": [
            "Flat ₹1,000 off with Boom promo code 'COFFEEBOOM'",
            "Free Aeroccino Milk Frother bundle discount"
        ]
    },
    {
        "id": 24,
        "title": "Samsonite 75cm Large Polycarbonate Hard Luggage Trolley (Midnight Blue)",
        "brand": "Samsonite",
        "category": "Home",
        "price": 13500,
        "original_price": 22500,
        "discount_percent": 40,
        "rating": 4.7,
        "rating_count": 5120,
        "image_url": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 25,
        "description": "Travel with unmatched security and effortless mobility. Samsonite's impact-resistant virgin polycarbonate shell protects your valuables, while 360-degree dual spinner wheels glide smoothly across airports.",
        "highlights": [
            "Dimensions: 75 x 52 x 31 cm | 108 Litres Large Capacity",
            "100% Makrolon Polycarbonate with scratch-resistant texture",
            "Integrated TSA combination lock for international travel peace of mind",
            "Double-wheel 360-degree silent spinner system",
            "Expandable zippered compartment for up to 15% extra packing volume"
        ],
        "specs": {
            "Size": "Large Check-in (75 cm / 28 inch)",
            "Weight": "4.1 kg",
            "Material": "Virgin Polycarbonate",
            "Lock": "TSA Accepted 3-Dial Combo",
            "Warranty": "10 Years Global Warranty"
        },
        "offers": [
            "Bank Offer: ₹1,500 Instant Discount on Axis Bank Credit Cards",
            "Free Samsonite Luggage Tag and Luggage Cover included"
        ]
    },
    {
        "id": 25,
        "title": "Kindle Paperwhite 11th Gen (16 GB, 6.8 inch 300 ppi Display with Warm Light)",
        "brand": "Amazon",
        "category": "Electronics",
        "price": 14999,
        "original_price": 17999,
        "discount_percent": 16,
        "rating": 4.6,
        "rating_count": 27800,
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80",
        "images": [
            "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&auto=format&fit=crop&q=80"
        ],
        "is_assured": 1,
        "stock": 40,
        "description": "Now with a 6.8-inch display and thinner borders, adjustable warm light, up to 10 weeks of battery life, and 20% faster page turns. Glare-free 300 ppi display that reads like real paper even in direct sunlight.",
        "highlights": [
            "6.8-inch 300 ppi glare-free Paperwhite display",
            "Adjustable Warm Light shifts screen shade from white to amber",
            "IPX8 waterproof to protect against accidental water immersion",
            "16 GB storage holds thousands of books",
            "Single charge via USB-C lasts up to 10 weeks"
        ],
        "specs": {
            "Screen Size": "6.8 inch glare-free screen",
            "Resolution": "300 ppi",
            "Battery Life": "Up to 10 weeks",
            "Storage": "16 GB",
            "Connectivity": "Wi-Fi (2.4 GHz and 5.0 GHz)",
            "Warranty": "1 Year Limited Brand Warranty"
        },
        "offers": [
            "Free 3 Months Kindle Unlimited Subscription",
            "Extra ₹1,000 off on Exchange of older e-reader"
        ]
    }
]

REVIEWS_SEED = [
    {"product_id": 1, "user_name": "Rohan Sharma", "rating": 5, "title": "Absolute beast of a smartphone!", "comment": "Upgraded from iPhone 12 and the titanium body feels so light and premium. Camera zoom is outstanding and battery easily lasts 1.5 days.", "verified": 1, "date": "15 Sep 2026"},
    {"product_id": 1, "user_name": "Priya Nair", "rating": 5, "title": "Worth every single rupee", "comment": "The natural titanium color is subtle and elegant. USB-C makes life so easy with my laptop charger. Boom delivered within 24 hours!", "verified": 1, "date": "10 Sep 2026"},
    {"product_id": 2, "user_name": "Vikram Sethi", "rating": 5, "title": "AI features are game changing", "comment": "Circle to search and instant translation work like magic. The screen is so bright outdoors without reflections. S-pen is super handy.", "verified": 1, "date": "18 Sep 2026"},
    {"product_id": 6, "user_name": "Ananya Roy", "rating": 5, "title": "Silent power machine", "comment": "M3 chip handles 4K video editing without a whisper of fan noise. Battery lasts whole workday without plugging in. Super lightweight!", "verified": 1, "date": "22 Sep 2026"},
    {"product_id": 10, "user_name": "Arjun Patel", "rating": 5, "title": "Best ANC on the market", "comment": "Cancelled out all airplane engine roar during my flight. Mics are also clear for Zoom calls. Very comfortable earcups.", "verified": 1, "date": "12 Sep 2026"},
    {"product_id": 13, "user_name": "Kavita Verma", "rating": 4, "title": "Crazy value for money", "comment": "For this price the bass and battery life are unbeatable. Great for daily workout and college commutes.", "verified": 1, "date": "05 Sep 2026"},
    {"product_id": 18, "user_name": "Sunny Gill", "rating": 5, "title": "Sneakerhead dream", "comment": "100% genuine Jordan 1s. Box was crisp and packaging was secured. Delivery was fast with Boom Assured badge!", "verified": 1, "date": "14 Sep 2026"}
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        brand TEXT NOT NULL,
        category TEXT NOT NULL,
        price INTEGER NOT NULL,
        original_price INTEGER NOT NULL,
        discount_percent INTEGER NOT NULL,
        rating REAL NOT NULL,
        rating_count INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        images_json TEXT NOT NULL,
        is_assured INTEGER NOT NULL DEFAULT 1,
        stock INTEGER NOT NULL,
        description TEXT NOT NULL,
        highlights_json TEXT NOT NULL,
        specs_json TEXT NOT NULL,
        offers_json TEXT NOT NULL
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        title TEXT NOT NULL,
        comment TEXT NOT NULL,
        verified INTEGER DEFAULT 1,
        date TEXT NOT NULL,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        pincode TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        total_amount INTEGER NOT NULL,
        total_discount INTEGER NOT NULL,
        items_json TEXT NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmed'
    )
    ''')

    # Seed products
    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]
    if count == 0:
        for p in PRODUCTS:
            cur.execute('''
            INSERT INTO products (
                id, title, brand, category, price, original_price,
                discount_percent, rating, rating_count, image_url,
                images_json, is_assured, stock, description,
                highlights_json, specs_json, offers_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                p["id"],
                p["title"],
                p["brand"],
                p["category"],
                p["price"],
                p["original_price"],
                p["discount_percent"],
                p["rating"],
                p["rating_count"],
                p["image_url"],
                json.dumps(p["images"]),
                p["is_assured"],
                p["stock"],
                p["description"],
                json.dumps(p["highlights"]),
                json.dumps(p["specs"]),
                json.dumps(p["offers"])
            ))

        for r in REVIEWS_SEED:
            cur.execute('''
            INSERT INTO reviews (product_id, user_name, rating, title, comment, verified, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                r["product_id"],
                r["user_name"],
                r["rating"],
                r["title"],
                r["comment"],
                r["verified"],
                r["date"]
            ))

    conn.commit()
    conn.close()
    print(f"Database initialized successfully with {len(PRODUCTS)} products.")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    init_db()
