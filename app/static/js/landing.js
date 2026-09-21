let slides = document.querySelectorAll(".slide");
let currentSlide = 0;

setInterval(function () {

    // Next image
    currentSlide++;

    if (currentSlide >= slides.length) {
        currentSlide = 0;
    }

    // Active class sirf next image ko do
    slides.forEach(function(slide) {
        slide.classList.remove("active");
    });

    slides[currentSlide].classList.add("active");

}, 1000);