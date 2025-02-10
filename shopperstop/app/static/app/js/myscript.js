$('.plus-cart').click(function(){
    var id= $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/pluscart/",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data =",data);
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function(){
    var id= $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/minuscart/",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.remove-cart').click(function(){
    var id= $(this).attr('pid').toString();
    var eml = this
    $.ajax({
        type:"GET",
        url:"/removecart/",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

$(document).on('click', '.plus-wishlist', function(){
    var id = $(this).data('pid');
    var url = $(this).data('url');
    var button = $(this);  // Store reference to the clicked button

    $.ajax({
        type: "GET",
        url: url,
        data: { prod_id: id },
        success: function(data){
            if (data.action === "added") {
                // Change button to remove from wishlist
                button.removeClass('plus-wishlist btn-success')
                      .addClass('minus-wishlist btn-danger')
                      .attr("data-url", "/minuswishlist")  // Change URL for future clicks
                      .html('<i class="fas fa-heart fa-lg"></i> '); // Update text

                // Add item to the wishlist section dynamically (if present)
                $('#wishlist-section').append(`
                    <div class="wishlist-item" data-id="${id}">
                        <p>Product ${id} added to wishlist</p>
                        <a href="#" class="remove-from-wishlist btn btn-danger" data-url="/minuswishlist" data-pid="${id}">
                            Remove
                        </a>
                    </div>
                `);
            }
        }
    });
});

$(document).on('click', '.minus-wishlist', function(){
    var id = $(this).data('pid');
    var url = $(this).data('url');
    var button = $(this);  // Store reference to the clicked button

    $.ajax({
        type: "GET",
        url: url,
        data: { prod_id: id },
        success: function(data){
            if (data.action === "removed") {
                // Change button to add to wishlist
                button.removeClass('minus-wishlist btn-danger')
                      .addClass('plus-wishlist btn-success')
                      .attr("data-url", "/pluswishlist")  // Change URL for future clicks
                      .html('<i class="fas fa-heart fa-lg"></i> '); // Update text

                // Remove item from wishlist section dynamically (if present)
                $(`.wishlist-item[data-id='${id}']`).remove();
            }
        }
    });
});

// Handling removal from wishlist section
$(document).on('click', '.remove-from-wishlist', function(){
    var id = $(this).data('pid');
    var url = $(this).data('url');

    $.ajax({
        type: "GET",
        url: url,
        data: { prod_id: id },
        success: function(data){
            if (data.action === "removed") {
                // Remove the wishlist item without refreshing
                $(`.wishlist-item[data-id='${id}']`).remove();

                // Update button if it's on the product page
                $(`a[data-pid='${id}']`).removeClass('minus-wishlist btn-danger')
                                         .addClass('plus-wishlist btn-success')
                                         .attr("data-url", "/pluswishlist")
                                         .html('<i class="fas fa-heart fa-lg"></i> Add to Wishlist');
            }
        }
    });
});
