const cart = new Map();
let products = [];
const money = value => new Intl.NumberFormat('es-CO', {style:'currency',currency:'COP',maximumFractionDigits:0}).format(value);

async function loadProducts() {
  const area = document.querySelector('#products');
  try {
    const response = await fetch('/api/products');
    if (!response.ok) throw new Error('No fue posible cargar el catálogo.');
    products = await response.json();
    area.replaceChildren();
    products.forEach(product => {
      const card = document.createElement('article'); card.className = 'product-card';
      const art = document.createElement('div'); art.className = 'product-art';
      const emoji = document.createElement('span'); emoji.textContent = product.emoji; art.append(emoji);
      const info = document.createElement('div'); info.className = 'product-info';
      const title = document.createElement('h3'); title.textContent = product.name;
      const description = document.createElement('p'); description.textContent = product.description;
      const bottom = document.createElement('div'); bottom.className = 'product-bottom';
      const price = document.createElement('span'); price.className = 'price'; price.textContent = money(product.price);
      const button = document.createElement('button'); button.className = 'add-btn'; button.textContent = 'Agregar +'; button.type = 'button';
      button.addEventListener('click', () => { cart.set(product.id, (cart.get(product.id) || 0) + 1); renderCart(); });
      bottom.append(price, button); info.append(title, description, bottom); card.append(art, info); area.append(card);
    });
  } catch (error) { area.textContent = error.message; }
}

function renderCart() {
  const area = document.querySelector('#cart-items'); area.replaceChildren();
  let count = 0, total = 0;
  if (!cart.size) { const empty = document.createElement('p'); empty.className = 'empty'; empty.textContent = 'Tu carrito está vacío.'; area.append(empty); }
  for (const [id, quantity] of cart) {
    const product = products.find(item => item.id === id); if (!product) continue;
    count += quantity; total += product.price * quantity;
    const row = document.createElement('div'); row.className = 'cart-row';
    const name = document.createElement('span'); name.textContent = `${product.name} × ${quantity}`;
    const price = document.createElement('strong'); price.textContent = money(product.price * quantity);
    const remove = document.createElement('button'); remove.className = 'remove-btn'; remove.type = 'button'; remove.setAttribute('aria-label', `Quitar ${product.name}`); remove.textContent = '×';
    remove.addEventListener('click', () => { cart.delete(id); renderCart(); }); row.append(name, price, remove); area.append(row);
  }
  document.querySelector('#cart-count').textContent = count;
  document.querySelector('#cart-total').textContent = money(total);
}

document.querySelector('#order-form').addEventListener('submit', async event => {
  event.preventDefault(); const feedback = document.querySelector('#feedback'); feedback.classList.remove('error');
  if (!cart.size) { feedback.textContent = 'Agrega al menos un producto para continuar.'; feedback.classList.add('error'); return; }
  const form = new FormData(event.currentTarget);
  const payload = {customer: form.get('customer'), email: form.get('email'), items: [...cart].map(([product_id, quantity]) => ({product_id, quantity}))};
  try {
    const response = await fetch('/api/orders', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const result = await response.json(); if (!response.ok) throw new Error(result.error || 'No se pudo registrar el pedido.');
    feedback.textContent = `¡Pedido #${result.order_id} registrado! Total: ${money(result.total)}.`;
    cart.clear(); renderCart(); event.currentTarget.reset();
  } catch (error) { feedback.textContent = error.message; feedback.classList.add('error'); }
});

loadProducts(); renderCart();
