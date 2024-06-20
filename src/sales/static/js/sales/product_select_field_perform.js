class ProductsField {
    constructor () {
        
    }
}


class SelectedProduct {
    
    constructor (productId, productName, selectedQuantity=1) {
        this.id = productId
        this.name = productName
        this.quantity = selectedQuantity
        this.container = document.getElementById("selected_products")
    }

    toDOMElement () {
        const productElement = `<p>${this.name}</p>
            <div>
                <input type='number' name='quantity_${this.id}' min='1' step='1' value='${this.quantity}' />
                <a id='delete'>retirer</a>
            </div>`;
        const container = document.createElement("div");
        container.classList.add("selected-product")
        container.innerHTML = productElement;
        container.querySelector("a#delete").addEventListener("click", this.deleteFromSelected.bind(this))
        return container;
    }

    addToSelected () {
        this.container.appendChild(this.toDOMElement())
    }

    deleteFromSelected (event) {
        // event.preventDefault();
        console.log(event.target)
    }
}
// const selectProduct = new SelectedProduct("plot")

document.getElementById("add_btn").addEventListener("click", (event) => {
    event.preventDefault();
    const productsField = document.querySelector("select#id_products");
    
    Array.from(productsField.options).forEach(option => {
        if (option.selected) {
            // console.log(option)
            const selectedProduct = new SelectedProduct(
                option.value,
                option.innerText,
            )
            selectedProduct.addToSelected()
        }
    })
    console.log()
})


