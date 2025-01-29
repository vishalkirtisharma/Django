// Check if there's an existing cart in localStorage
if (localStorage.getItem('cart') === null || localStorage.getItem('cart') === ''  ) {
    // If no cart exists, initialize an empty cart object
    var cart = {};
} else {
    // If a cart exists, retrieve it from localStorage and parse it into an object
    cart = JSON.parse(localStorage.getItem('cart'));
}

// Select all elements with the class 'add_cart' (for buttons or links that add items to the cart)
let add_cart = document.querySelectorAll('.add_cart');

// Loop through each element selected and attach a 'click' event listener


add_cart.forEach(function(element) {
    element.addEventListener('click', function() {
        // Get the item ID from the clicked element (assuming the ID is unique to each item)
        var item_id = element.id.toString();
        
        // Check if the item is already in the cart
        if (cart[item_id] !== undefined) {
            // If the item exists, increase the quantity by 1
            cart[item_id][0]++;


        } else {
            // If the item doesn't exist in the cart, add it with a quantity of 1
            quantity = 1;
            name = document.getElementById('nm' + item_id).innerHTML
            img_src = document.getElementById('img' + item_id).src
            price = parseFloat( document.getElementById('pr' + item_id).innerHTML.slice(1))
            cart[item_id] = [quantity, name, img_src,price];
        }

        // you can save the updated cart back to localStorage:
        localStorage.setItem('cart', JSON.stringify(cart));

        document.getElementById('cart').innerHTML = Object.keys(cart).length;
        cart_items.innerHTML =''
        display_cart(cart)            
    });
});

window.onload = function() {
    // Code you want to run when the page is refreshed
    document.getElementById('cart').innerHTML = Object.keys(cart).length;

};


const cart_items = document.getElementById('cart_items');

function display_cart(cart) {
let cartString = ''; // Initialize the cartString
let cartIndex = 1;   // Start cartIndex from 1

for (let x in cart) {
    cartString += `
    <div class="flex items-center space-x-4 py-2 border-b border-gray-200">
        <!-- Display cart index -->
        <span class="text-sm font-bold text-gray-700">${cartIndex}.</span>

        <!-- Item image -->
        <img src="${cart[x][2]}" alt="Item ${cartIndex}" class="w-12 h-12 object-cover rounded-md">

        <!-- Item details -->
        <div class="flex-1">
            <p class="text-sm font-semibold text-gray-800">${cart[x][1]}</p>
            <p class="text-sm text-gray-600">Qty: ${cart[x][0]}</p>
        </div>
    </div>
    `;

    cartIndex++; // Increment the cart index for the next item
}

// Update the cart_items element with the generated cartString
cart_items.innerHTML = cartString;
}

    
display_cart(cart)
    

        

