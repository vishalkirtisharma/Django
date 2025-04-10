$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        var food_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');
        
        var data = {
            food_id: food_id,
        };
        
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                // Handle success response here
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Handle error here
                console.error(error);
            }
        });
    });


    $('item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');

    })
});


