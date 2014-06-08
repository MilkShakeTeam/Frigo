var Product = {

    init: function() {
        this.bindEvents();
    },

    bindEvents: function() {
        $("#product_delete").on('click', this._deleteProduct);
    },

    _deleteProduct: function(e) {
        if ( !confirm('Supprimer le produit ?') ) e.preventDefault();
    }

}

$(function() {
    Product.init();
});