// Boom E-Commerce - Main JS Scripts (Flipkart UX)

// Toast Notification Utility
function showToast(message, type = 'success') {
  let toast = document.getElementById('fk-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'fk-toast';
    document.body.appendChild(toast);
  }

  const icon = type === 'success' ? 'bi-check-circle-fill' : (type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill');
  toast.className = `show ${type}`;
  toast.innerHTML = `<i class="bi ${icon}"></i> <span>${message}</span>`;

  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => {
    toast.className = '';
  }, 3200);
}

// Fallback image generator
function handleImageError(img, title = 'Boom Product') {
  img.onerror = null;
  const encodedTitle = encodeURIComponent(title.substring(0, 30));
  img.src = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300"><rect fill="%23f8f9fa" width="300" height="300"/><text fill="%232874f0" font-family="Arial, sans-serif" font-size="20" font-weight="bold" x="50%" y="45%" text-anchor="middle">BOOM</text><text fill="%23878787" font-family="Arial, sans-serif" font-size="12" x="50%" y="55%" text-anchor="middle">${encodedTitle}</text></svg>`;
}

// Add to Cart via AJAX
function addToCart(productId, quantity = 1, redirectCart = false) {
  fetch('/api/cart/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // Update badge
      const badges = document.querySelectorAll('.cart-counter-badge');
      badges.forEach(badge => {
        badge.textContent = data.cart_count;
        badge.style.display = data.cart_count > 0 ? 'inline-block' : 'none';
      });

      if (redirectCart) {
        window.location.href = '/cart';
      } else {
        showToast("Added to Cart successfully! 🛒", "success");
      }
    } else {
      showToast(data.message || "Failed to add to cart", "error");
    }
  })
  .catch(err => {
    console.error("Cart error:", err);
    showToast("Network error. Please try again.", "error");
  });
}

// Toggle Wishlist via AJAX
function toggleWishlist(productId, btnElement) {
  fetch('/api/wishlist/toggle', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ product_id: productId })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // Update badge
      const badges = document.querySelectorAll('.wishlist-counter-badge');
      badges.forEach(badge => {
        badge.textContent = data.wishlist_count;
        badge.style.display = data.wishlist_count > 0 ? 'inline-block' : 'none';
      });

      if (btnElement) {
        if (data.in_wishlist) {
          btnElement.classList.add('active');
          const icon = btnElement.querySelector('i');
          if (icon) {
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill');
          }
        } else {
          btnElement.classList.remove('active');
          const icon = btnElement.querySelector('i');
          if (icon) {
            icon.classList.remove('bi-heart-fill');
            icon.classList.add('bi-heart');
          }
        }
      }
      showToast(data.message, data.in_wishlist ? "success" : "info");
    }
  })
  .catch(err => {
    console.error("Wishlist error:", err);
  });
}

// Update Cart Item Quantity
function updateCartQty(productId, action) {
  fetch('/api/cart/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId, action: action })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      window.location.reload();
    }
  });
}

// Check Pincode simulation
function checkPincode() {
  const input = document.getElementById('pincode-input');
  const resultDiv = document.getElementById('pincode-result');
  if (!input || !resultDiv) return;

  const val = input.value.trim();
  if (!val) {
    resultDiv.innerHTML = '<span class="text-danger small">Please enter a pincode</span>';
    return;
  }

  fetch('/api/check-pincode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pincode: val })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      resultDiv.innerHTML = `
        <div class="mt-2 text-success small font-weight-bold">
          <i class="bi bi-truck"></i> ${data.message}
        </div>
      `;
    } else {
      resultDiv.innerHTML = `
        <div class="mt-2 text-danger small">
          <i class="bi bi-x-circle"></i> ${data.message}
        </div>
      `;
    }
  });
}

// Product Detail Image Switcher
function switchProductImage(thumbElement, newSrc) {
  const mainImg = document.getElementById('main-product-img');
  if (mainImg) {
    mainImg.src = newSrc;
  }
  document.querySelectorAll('.thumb-item').forEach(el => el.classList.remove('active'));
  if (thumbElement) {
    thumbElement.classList.add('active');
  }
}

// Submit Review via AJAX
function submitReview(productId) {
  const name = document.getElementById('review-user-name')?.value || 'Verified Customer';
  const rating = document.getElementById('review-rating')?.value || 5;
  const title = document.getElementById('review-title')?.value || '';
  const comment = document.getElementById('review-comment')?.value || '';

  if (!title.trim() || !comment.trim()) {
    showToast("Please provide both a title and comment.", "error");
    return;
  }

  fetch('/api/review/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_id: productId,
      user_name: name,
      rating: rating,
      title: title,
      comment: comment
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      showToast("Thank you! Review posted.", "success");
      setTimeout(() => {
        window.location.reload();
      }, 1200);
    } else {
      showToast(data.message || "Could not post review", "error");
    }
  });
}

// Auto carousel rotation
document.addEventListener('DOMContentLoaded', () => {
  const carouselEl = document.getElementById('heroCarousel');
  if (carouselEl && window.bootstrap && window.bootstrap.Carousel) {
    new bootstrap.Carousel(carouselEl, {
      interval: 4000,
      ride: 'carousel',
      pause: 'hover'
    });
  }
});
