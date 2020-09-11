$(window).load(()=>{
    $('#img_gallery').css("display","block");
});
$(document).ready(()=>{
    var limit=3;
    var len =$('.slick-carousel').find('img')
    $('.slick-stage').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.slick-carousel'
    });

    limit = (len.length == limit)? 2:(len.length < limit)? 1:3;
    
    $('.slick-carousel').slick({
        swipeToSlide:true,
        touchMove:true,
        slidesToShow: limit,
        slidesToScroll: 1,
        asNavFor: '.slick-stage',
        dots: false,
        infinite:false,
        centerMode: true,
        margin:0,
        focusOnSelect: true
    });
    
    

    $('#buy').on("click",()=>{
        let price = parseFloat($('#product_details #product_price').text().split(' ')[1].replace(',',''))
        let free_shipping = $('#product_details #product_shipping_price').text().split(' ')[0].toLowerCase()=="free";
        if(!free_shipping)   
        {
            shipping_price = parseFloat($('#product_details #product_shipping_price').text().split(' ')[1].replace(',',''));
            price += shipping_price;
        }
        let data = {
            "title" : $('#product_details #product_title').text(),
            "price" : parseInt(price),
            "img" : $('.image-listing img')[0].src,
            "quantity" : $('#quantity').val(),
            "id" : window.location.pathname.split('/')[2]
        }
        updateCart(data);      
    })
    

    
})
