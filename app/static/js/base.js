document.addEventListener("DOMContentLoaded", function(){

    // 🔹 IMAGE HOVER (TOP IMAGES)
    const img = document.querySelector('.img1');
    if(img){
        img.addEventListener('mouseenter', () => {
            img.src = "/static/images/img1r.jpg";
        });
        img.addEventListener('mouseleave', () => {
            img.src = "/static/images/img1.jpg";
        });
    }

    const img2 = document.querySelector('.img2');
    if(img2){
        img2.addEventListener('mouseenter', () => {
            img2.src = "/static/images/img2r.jpg";
        });
        img2.addEventListener('mouseleave', () => {
            img2.src = "/static/images/img2.jpg";
        });
    }

    // 🔹 NAVBAR HOVER BOXES
    const setupHover = (trigger, box) => {
        if(!trigger || !box) return;

        let timeout;

        trigger.addEventListener('mouseenter', () => {
            clearTimeout(timeout);
            box.style.display = 'block';
        });

        trigger.addEventListener('mouseleave', () => {
            timeout = setTimeout(() => {
                box.style.display = 'none';
            }, 300);
        });

        box.addEventListener('mouseenter', () => {
            clearTimeout(timeout);
        });

        box.addEventListener('mouseleave', () => {
            timeout = setTimeout(() => {
                box.style.display = 'none';
            }, 300);
        });
    };

    setupHover(
        document.querySelector('.category-item'),
        document.querySelector('.hover-box')
    );

    setupHover(
        document.querySelector('.category-item2'),
        document.querySelector('.hover-box2')
    );

    setupHover(
        document.querySelector('.category-item3'),
        document.querySelector('.hover-box3')
    );

    // 🔹 PRODUCT CARDS (SEARCH BOX)
    const setupProductHover = (cardClass, imgClass, hoverImg, normalImg) => {
        const card = document.querySelector(cardClass);
        const image = document.querySelector(imgClass);

        if(!card || !image) return;

        card.addEventListener('mouseenter', () => {
            image.src = hoverImg;
        });

        card.addEventListener('mouseleave', () => {
            image.src = normalImg;
        });
    };

    setupProductHover('.product-card', '.product-img1',
        "/static/images/img4b.jpg", "/static/images/img4.jpg");

    setupProductHover('.product-card2', '.product-img2',
        "/static/images/img3b.jpg", "/static/images/img3.jpg");

    setupProductHover('.product-card3', '.product-img3',
        "/static/images/img5b.jpg", "/static/images/img5.jpg");

    setupProductHover('.product-card4', '.product-img4',
        "/static/images/img6b.jpg", "/static/images/img6.jpg");

    // 🔹 SEARCH BOX (MAIN FIX)

//     const searchBtn = document.getElementById("search-logo");
//     const searchBox = document.querySelector(".search-box");

//     if(searchBtn && searchBox){

//         searchBtn.addEventListener("click", function(e){
//             e.stopPropagation();
//             searchBox.style.display = "block";
//         });

//         document.addEventListener("click", function(){
//             searchBox.style.display = "none";
//         });

//         searchBox.addEventListener("click", function(e){
//             e.stopPropagation();
//         });
//     }

});