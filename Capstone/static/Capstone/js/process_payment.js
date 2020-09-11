// Disable all click events.
document.addEventListener("click",handler,true)
function handler(e){
    if(e.target.classList[0]!="navigate-back")
    {
        e.stopPropagation();
        e.preventDefault();
    }
}

function orderStatus(id,status)
{
    localStorage.clear();
    data =new FormData();
    data.append("id",id)
    data.append("status",status)
    fetch(url,{
        method:"POST",
        credentials:"same-origin",
        body:data,
        headers:{'X-CSRFToken':csrftoken},
    })
    
}
// Render the PayPal button into #paypal-button-container
paypal.Buttons({            
    onCancel: function (data) {
        // Show a cancel page, or return to cart
        orderStatus(order_id,"failed");
        alert('Transaction cancelled');
        window.location.pathname = "payment-cancelled/";  
    },

    style: {
        color:  'blue',
        shape:  'pill',
        label:  'pay',
        height: 40
    },

    // Set up the transaction
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: total
                }
            }]
        });
    },

    // Finalize the transaction
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            orderStatus(order_id,"success");
            // Show a success message to the buyer
            alert('Transaction completed by ' + details.payer.name.given_name + '!');
            
            window.location.pathname = "payment-done/";

        });
    }


}).render('#paypal-button-container');

$(window).bind("beforeunload",()=>{
    alert("are you sure?")
})