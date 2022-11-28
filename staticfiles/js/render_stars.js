"use strict";
console.log('PD LIST JS LOADED')


const renderRatings = (rating) => {

    let stars;

    // 0 to 0.5
    if (rating >= 0.0 && rating < 0.5) {
        stars = `
                        <span class="h6 text-gray-500"> ( No ratings ) </span>
                        `
    }

    // 0.5 to 1.0
    if (rating >= 0.5 && rating < 1.0) {
        stars = ` 
                        <i class="fas fa-star-half-alt">  
                        `
    }

    // 1.0 to 1.5
    if (rating >= 1.0 && rating < 1.5) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star-half-alt">  
                        `
    }

    // 1.5 to 2.0
    if (rating >= 1.5 && rating < 2.0) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star-half-alt">  
                        `
    }

    // 2.0 to 2.5
    if (rating >= 2.0 && rating < 2.5) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        `
    }

    // 2.5 to 3.0
    if (rating >= 2.5 && rating < 3.0) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star-half-alt">
                        `
    }

    // 3.0 to 3.5
    if (rating >= 3.0 && rating < 3.5) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i> 
                        `
    }

    // 3.5 to 4.0
    if (rating >= 3.5 && rating < 4.0) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star-half-alt">
                        `
    }

    // 4.0  to 4.5
    if (rating >= 4.0 && rating < 4.5) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i>
                        `
    }

    // 4.5  to 4.5
    if (rating >= 4.5 && rating < 5.0) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star-half-alt">
                        `
    }

    // 5.0
    if (rating >= 4.5 && rating < 5.0) {
        stars = ` 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i> 
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        `
    }






    return stars
};


const product_ratings = document.querySelectorAll('.product__rating');


product_ratings.forEach((rating) => {
    let product_rating = Number(rating.textContent);
    let res = renderRatings(product_rating);
    rating.classList.remove('hidden');

    rating.innerHTML = '';
    rating.innerHTML = res;
})