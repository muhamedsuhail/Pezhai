var cart_items;
var cart_total;
var csrftoken = Cookies.get('csrftoken'); //Django csrf validation
var path=window.location.pathname;
var click_event = (/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) ? 'touchstart' : 'click'; 

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function updateLocalStorage(data1,data2)
{
    localStorage.setItem('cart-items',JSON.stringify(data1));
    cart_items = JSON.parse(localStorage.getItem('cart-items'));
    localStorage.setItem('cart-total',data2);
    cart_total = parseInt(localStorage.getItem('cart-total'));
    return [cart_items,cart_total];
}

function cartTotalUpdate(cart_total,cart_items)
{
    if(cart_items.length!=0)
    {
        $('.checkout').each(function(){
            $(this).find('.btn').removeClass('disabled');
        })
    }
    else
    {
        $('.checkout').each(function(){
            $(this).find('.btn').addClass('disabled');
        })
    }

    if(cart_total==0|cart_total)
    {
        tot = numberWithCommas(cart_total)
        $('.cart-total').html(`₹ ${tot}`);      
    }
    else
    {
        cart_total = 0;
    }

    if(cart_items)
    {
        $('.cart-items').html(cart_items.length);
    }

    return
}

function updateToServer(cart_items,cart_total,args='',target=0)
{
    cartTotalUpdate(cart_total,cart_items);
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);
    fdata= new FormData();
    fdata.append("tag","updateCart")
    fdata.append("data",JSON.stringify({'cart_items':cart_items,'cart_total':cart_total,'args':args,'target':target}))
    fetch("/",{
        method:"POST",
        credentials:'same-origin',
        body:fdata,
        headers:headers,
    })
    .then(response=>{
        return response.json();
    })
}


function cartUpdate()
{
    var cart_items = JSON.parse(localStorage.getItem('cart-items'))
    var cart_total = parseInt(localStorage.getItem('cart-total'))
    if(cart_items)
    {
        updateToServer(cart_items,cart_total);
    }
    var headers = new Headers();
    headers.append('X-CSRFToken', csrftoken);
    data = new FormData()
    data.append("tag","getCartItems")
    fetch("/",{
        method:"POST",
        body:data,
        credentials:'same-origin',
        headers:headers,
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data["status"]=="success" && data['User_Authenticated']==true)
        {
            if(data["cart_items"].length!=0)
            {
                
                cart = updateLocalStorage(data["cart_items"],data["cart_total"]);
                cart_items = cart[0];
                cart_total = cart[1];
                
                $('.cart-items').html(cart_items.length);
                for(i of cart_items)
                {
                    pushToCart(i);
                }
            }
            else
            {
                cart = updateLocalStorage(Array(),0);
                cart_items = cart[0];
                cart_total = cart[1];
            }
        }
        else
        {
            if(!cart_items)
            {
                cart = updateLocalStorage(Array(),0);
                cart_items = cart[0];
                cart_total = cart[1];
                
            }
            else 
            {
                
                for(i of cart_items)
                {
                    pushToCart(i);
                }
            }
        }
        cartTotalUpdate(cart_total,cart_items);
    })
    
}

function updateCart(data)
{
    cart_items = JSON.parse(localStorage.getItem('cart-items'))
    cart_total = parseInt(localStorage.getItem('cart-total'))
    var item_exists=false;
    for(i of cart_items)
    {
        if(i["id"]==data["id"])
        {
            cart_total -= parseInt(i["quantity"]*i["price"])
            i["quantity"] = data["quantity"];
            $('.cart').each(function(){$(this).find(`.item${data["id"]} .item-quantity`).html(i["quantity"])})
            item_exists = true;
        }
    }
    if(!item_exists)
    {
        pushToCart(data);
        cart_items.push(data);
        $('.cart-items').html(parseInt($('.cart-items').html())+1);
    }
    cart_total += parseInt(data["price"]*data["quantity"]);
    cart =  updateLocalStorage(cart_items,cart_total);
    cart_items = cart[0];
    cart_total = cart[1];
    tot = numberWithCommas(cart_total);
    $('.cart-total').html(`₹ ${tot}`);
    updateToServer(cart_items,cart_total);
}

function pushToCart(data)
{
    
    let price = numberWithCommas(data["price"]);
    var item = `
                    <li class="item item${data["id"]}">
                        <div class="cart-img">
                            <img src="${data["img"]}" alt="img">
                        </div>
                        <div class="cart-details">
                            <div class="cart_title"><a style="text-decoration:none;color:black" href="/product/${data["id"]}"><b>${data["title"].slice(0,35)}...</b></a></div>
                            <div>₹ ${price}</div>
                            <div style="opacity:0.5">Quantity:<span class="item-quantity">${data["quantity"]}</span></div>
                            <div class="item-remove"><i class="fa fa-close"></i></div>
                        </div>
                    </li>
                `
    $('.cart').each(function(){$(this).append(item)})
    
    $(`.item${data["id"]} .item-remove`).click((e)=>{
        
        $(`.item${data["id"]}`).hide(easings="swing")
        cart_items = JSON.parse(localStorage.getItem('cart-items'))
        cart_total = localStorage.getItem('cart-total');
        for(i of cart_items)
        {   
            if(i.id==data["id"])
            {
                var target = cart_items.indexOf(i);
                cart_total -= parseInt(i["price"]*i["quantity"]);
                break
            }
        }
        
        cart_items.splice(target,1);
        cart = updateLocalStorage(cart_items,cart_total);
        cart_items = cart[0];
        cart_total = cart[1];
        updateToServer(cart_items,cart_total,'remove',target);  
    })

}

$(document).ready(()=>{
    cartUpdate();
    $('#shopping-cart-icon').on("click",()=>{
            if(click_event=='touchstart')
            {
                $('#shopping-cart').modal("toggle");
            }
            else
            {
                $(".shopping-cart").fadeToggle("fast");
                
                $('.shopping-cart').hover(
                    function() {
                        
                    }, function() {
                        $('.shopping-cart').fadeOut("fast");
                    })
            }
    });

    var open = false;
    $('.menu').on("click",()=>{
            if(!open)
            {
                $('.side-nav').show();
                $('.menu').addClass('open')
                $('.side-nav').addClass('open')
                open = true;
                $('html, body').css({
                    overflow: 'hidden',
                    height: '100%'
                });                
            }
            else
            {
                $('#nav-links').hide();
                $('.menu').removeClass('open')
                $('.side-nav').removeClass('open')
                open = false;
                $('html, body').css({
                    overflow: 'auto',
                    height: 'auto'
                });
            }
    });


    $("#user-icon").on("click",function(){
        $( "#user-options" ).slideToggle("fast");
        
        $( "#user-options" ).hover(
            function() {
                
            }, function() {
                $( "#user-options" ).slideUp("fast");
            }
            );
    });

    $('#nav-trigger').on("click",()=>{
        $('#nav-links').slideToggle("fast");
    });
    [".logout",".login"].forEach(i=>{
        $(i).each(function(){
            $(this).on("click",()=>{
                localStorage.clear();
            })
        })       
    })
})