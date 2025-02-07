// Custom JS
"use strict";
var n = jQuery.noConflict();
function isotopAutoSet() {

    // Woo categories
    jQuery(".category-carousel").each(function() {
        "use strict";
        if (n(this).attr("id")) {
            var e = n(this).attr("id").replace("_category_carousel", "");
            n(".category-carousel").addClass("owl-carousel");
            n(".category-carousel").owlCarousel({
                navigation: true,
                pagination: false,
                items: e,
                itemsLarge: [1400, 6],
                itemsDesktop: [1200, 5],
                itemsDesktopSmall: [979, 3],
                itemsTablet: [640, 2],
                itemsMobile: [479, 2]
            })
        }
    });
	

    // Testimonials
    jQuery(".testimonial-carousel").each(function() {
        "use strict";
            n(".testimonial-carousel .elementor-widget-wrap").addClass("owl-carousel");
            n(".testimonial-carousel .elementor-widget-wrap").owlCarousel({
                navigation: true,
                pagination: false,
                autoplay:1000,
                items: 3,
                itemsLarge: [1400, 3],
                itemsDesktop: [1200, 3],
                itemsDesktopSmall: [979, 2],
                itemsTablet: [600, 1],
                itemsMobile: [479, 1]
            })
    });	

    


    jQuery(".homepage-brand-slider").each(function() {
        "use strict";
            n(".homepage-brand-slider .brand-slider").addClass("owl-carousel");
            n(".homepage-brand-slider .brand-slider").owlCarousel({
                navigation: true,
                pagination: false,
                autoplay:1000,
                items: 6,
                itemsLarge: [1400, 4],
                itemsDesktop: [1200, 3],
                itemsDesktopSmall: [979, 3],
                itemsTablet: [600, 2],
                itemsMobile: [479, 2]
            })
    });	

    // Blog
    jQuery(".blog-carousel").each(function() {
        "use strict";
        if (n(this).attr("id")) {
            var e = n(this).attr("id").replace("_blog_carousel", "");
            n(".blog-carousel").addClass("owl-carousel");
            n(".blog-carousel").owlCarousel({
                navigation: true,
                pagination: false,
                items: e,
                itemsLarge: [1400, e],
                itemsDesktop: [1200, e],
                itemsDesktopSmall: [979, 2],
                itemsTablet: [600, 2],
                itemsMobile: [479, 1]
            })
        }
    });

    jQuery(".hot-product").each(function() {
        "use strict";
        if (n(this).attr("id")) {
            var e = n(this).attr("id").replace("_hot_product_carousel", "");
            n(".hot-product ul.products").addClass("owl-carousel");
            n(".hot-product ul.products").owlCarousel({
                navigation: true,
                pagination: false,
                afterAction: function(el){
                    //remove class active
                    this
                    .$owlItems
                    .removeClass('first active')
                    let a = 1;
                    //add class active
                    this
                    .$owlItems //owl internal $ object containing items
                    .eq(this.currentItem)
                    .addClass('first active')  
                    
                    //remove class active
                    this
                    .$owlItems
                    .removeClass('last active')
                    let b = 1;
                    let z = e -b;
                    //add class active
                    this
                    .$owlItems //owl internal $ object containing items
                    .eq(this.currentItem + z)
                    .addClass('last active')     
                },
                items: 3,
                itemsLarge: [1400, 3],
                itemsDesktop: [1200, 3],
                itemsDesktopSmall: [979, 2],
                itemsTablet: [600, 1],
                itemsMobile: [479, 1]
            })
        }
    });

    // Products
    jQuery(".woo-carousel").each(function() {
        "use strict";
        if (n(this).attr("id")) {
            var e = n(this).attr("id").replace("_woo_carousel", "");
            var t = n(this).find("ul.products .product").length;
            if (t > e) {
                n(this).find("ul.products").addClass("owl-carousel");
                n(this).find("ul.products").owlCarousel({
                    navigation: true,
                    pagination: false,
                    afterAction: function(el){
                        //remove class active
                        this
                        .$owlItems
                        .removeClass('first active')
                        let a = 1;
                        //add class active
                        this
                        .$owlItems //owl internal $ object containing items
                        .eq(this.currentItem)
                        .addClass('first active')  
                        
                        //remove class active
                        this
                        .$owlItems
                        .removeClass('last active')
                        let b = 1;
                        let z = e -b;
                        //add class active
                        this
                        .$owlItems //owl internal $ object containing items
                        .eq(this.currentItem + z)
                        .addClass('last active')     
                    },
                    items: e,
                    itemsLarge: [1400, 5],
                    itemsDesktop: [1250, 4],
                    itemsDesktopSmall: [979, 3],
                    itemsTablet: [640, 2],
                    itemsMobile: [478, 2]
                })
            }
        }
    });

    // Related Product
    jQuery(".related ul.products li").each(function() {
        "use strict";
            n(".related ul.products").addClass("owl-carousel");
            n(".related ul.products").owlCarousel({
                navigation: true,
                pagination: false,
                autoplay:1000,
                items: 5,
                itemsLarge: [1400, 5],
                itemsDesktop: [1200, 4],
                itemsDesktopSmall: [979, 3],
                itemsTablet: [600, 2],
                itemsMobile: [479, 2]
            })
    });	

    // Upsells Product
    jQuery(".upsells ul.products li").each(function() {
        "use strict";
            n(".upsells ul.products").addClass("owl-carousel");
            n(".upsells ul.products").owlCarousel({
                navigation: true,
                pagination: false,
                autoplay:1000,
                items: 7,
                itemsLarge: [1400, 5],
                itemsDesktop: [1200, 4],
                itemsDesktopSmall: [979, 3],
                itemsTablet: [600, 2],
                itemsMobile: [479, 2]
            })
    });	 
    
    // Cross-Sells Product
    jQuery(".cross-sells ul.products li").each(function() {
        "use strict";
            n(".cross-sells ul.products").addClass("owl-carousel");
            n(".cross-sells ul.products").owlCarousel({
                navigation: true,
                pagination: false,
                autoplay:1000,
                items: 7,
                itemsLarge: [1400, 3],
                itemsDesktop: [1200, 3],
                itemsDesktopSmall: [979, 2],
                itemsTablet: [600, 2],
                itemsMobile: [479, 2]
            })
    });	 


    function singleproductcarousel() {
        "use strict";
        jQuery('.product .flex-control-thumbs').addClass('owl-carousel');
        jQuery(".product .flex-control-thumbs").owlCarousel({
            navigation: true,
            pagination: false,
            items: 4,
            itemsDesktop: [1299, 3],
            itemsDesktopSmall: [991, 3],
            itemsTablet: [600, 2],
            itemsMobile: [479, 2]
        });
    }
    
    jQuery(document).ready(function() {  "use strict";  singleproductcarousel() });
    jQuery(window).load(function() {  "use strict";	singleproductcarousel() });
    jQuery(window).resize(function() {  "use strict";singleproductcarousel()});

}
// jQuery(document).ready(function() {  "use strict";  isotopAutoSet() });
jQuery(window).on('load',function() {  "use strict";  isotopAutoSet()});
jQuery(window).resize(function() { "use strict"; isotopAutoSet()});
jQuery(window).on('load',function() {  
    jQuery(".pageloader").fadeOut("slow");
});


jQuery(window).on('load', function() {
    "use strict";
    var $height = 0 ;
    jQuery(".product-action-wrap").each(function(){
   if((jQuery(this).height())>$height){
    $height = jQuery(this).height();
    }
    });
    jQuery("ul.products.woo-archive-action-on-hover .woo-archive-outer").each(function(){
    jQuery(this).css("margin-bottom",-$height - 6);
    jQuery(this).css("padding-bottom",$height + 6);
	jQuery("ul.align-buttons-bottom .product-action-wrap").css("bottom", -$height - 6);
    });
	    
    jQuery('.side-mobile-toggle-open-container').on("click",function() {
        jQuery(".primary-sidebar").addClass("active");
        jQuery(this).toggleClass("active");
    });
    jQuery('.base-hide-sidebar-btn #menu-toggle-icon').on("click",function() {
        jQuery(".primary-sidebar").removeClass("active");
        jQuery('.side-mobile-toggle-open-container').removeClass("active");
    });
});
jQuery('.widget_block').on("click",function() {
    jQuery('.product-categories').slideToggle("slow");
});

 // JS for adding menu more link in navigation
function moreTab() {
    "use strict";
    var max_elem = 8;
    if (jQuery(window).width() < 1350) {
        var max_elem = 4;
    }
    jQuery('#site-navigation').addClass('more');
    var items = jQuery('#site-navigation.more .menu > li');
    var surplus = items.slice(max_elem, items.length);
    surplus.wrapAll('<li class="menu-item menu-item-type-post_type menu-item-object-page hiden_menu menu-item-has-children menu-item--has-toggle"><ul class="sub-menu">');
    jQuery('.hiden_menu').prepend('<a href="#" class="level-0  activSub">More</a>');
}
jQuery(document).ready(function() {
    "use strict";
    moreTab()
});

// JS toggle for sidebar and footer
function SidebarFooterToggle() {
    "use strict";
    jQuery('footer .widget h3,footer .widget .wp-block-heading ,footer .woocommerce-shipping-calculator .shipping-calculator-button, .dropdown-toggle-nav .widget_product_categories .widgettitle').parent().addClass('toggled-off');
    jQuery('footer .widget h3,footer .widget .wp-block-heading ,footer .woocommerce-shipping-calculator .shipping-calculator-button, .dropdown-toggle-nav .widget_product_categories .widgettitle').on("click", function() {
        if (jQuery(this).parent().hasClass('toggled-on')) {
            jQuery(this).parent().removeClass('toggled-on');
            jQuery(this).parent().addClass('toggled-off');            
        } else {
            jQuery(this).parent().addClass('toggled-on');
            jQuery(this).parent().removeClass('toggled-off');            
        }
        return (false);
    });    
}
jQuery(document).ready(function() {
    "use strict";
    SidebarFooterToggle()
});


/* category more and less tab */
jQuery(document).ready(function(){
    var max_elem = 10, i = 0;
    var itemstop = jQuery('.dropdown-toggle-nav .product-categories > li.cat-item');  
    if ( itemstop.length > max_elem ) {
       jQuery('.dropdown-toggle-nav .product-categories').append('<li class="cat-item"><div class="more-wrap"><span class="more-view">Show More</span></div></li>');
    }
    jQuery('.dropdown-toggle-nav .product-categories .more-wrap').on( "click",function() {
        if (jQuery(this).hasClass('active')) {
            itemstop.each(function(i) {
                if ( i >= max_elem ) {
                    jQuery(this).slideUp(600);
                }
            });
            jQuery(this).removeClass('active');
                jQuery('.more-wrap').html('<span class="more-view">Show More</span>');
            } else {
                itemstop.each(function(i) {
                    if ( i >= max_elem  ) {
                        jQuery(this).slideDown(600);
                    }
                });
                jQuery(this).addClass('active');
                jQuery('.more-wrap').html('<span class="more-view">Show Less</span>');
            }
        });
    itemstop.each(function(i) {
        if ( i >= max_elem ) { 
            jQuery(this).css('display', 'none');
        }
    });
});

