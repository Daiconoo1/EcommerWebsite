 $(document).ready(function(){

  $('.product-wrapper').slick({
  slidesToShow: 4,
  slidesToScroll: 1,
  speed:4000,
  autoplay: true,
  infinite: true,
  autoplaySpeed: 2000,
  nextArrow: $('.next'),
  prevArrow: $('.prev'),
  mobileFirst: true,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
        dots: true,
		 
		 
      }
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
		centerMode:false,
      }
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
		 
      }
    },
    {
      breakpoint: 360,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
     
      }
    },
    {
      breakpoint: 320,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
     
      }
    }
     
  ]
   
});

$('.firstImage-wrapper').slick({
  
  infinite: true,
  autoplay: true,
  speed:2000,
  autoplaySpeed: 3700,
  nextArrow: $('.nexxtt'),
  prevArrow: $('.previs'),   
  fade: true,
  cssEase: 'linear'
});

$('.image_slider').slick({
  
  infinite: true,
  nextArrow: $('.nextt'),
  prevArrow: $('.previous'),
  speed: 500,
  fade: true,
  cssEase: 'linear'
});
	
});





