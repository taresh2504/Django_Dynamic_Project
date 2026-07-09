document.querySelectorAll(".filter-btn").forEach(btn => {

    btn.addEventListener("click", function(e){

        const dropdown = this.nextElementSibling
        const arrow = this.querySelector("#arrow")

        document.querySelectorAll(".dropdown").forEach(d => {
            if(d !== dropdown){
                d.style.display = "none"
            }
        })

        document.querySelectorAll("#arrow").forEach(a=>{
            if(a !== arrow){
                a.classList.remove("rotate")
            }
        })

        if(dropdown.style.display === "block"){
            dropdown.style.display = "none"
            arrow.classList.remove("rotate")
        }else{
            dropdown.style.display = "block"
            arrow.classList.add("rotate")
        }

        e.stopPropagation()
    })
})

document.addEventListener("click", ()=>{
    document.querySelectorAll(".dropdown").forEach(d=>{
        d.style.display="none"
    })

    document.querySelectorAll(".arrow").forEach(a=>{
        a.classList.remove("rotate")
    })
})

// Product type 

// Product type checkbox logic
const checkboxes = document.querySelectorAll(".ptype");
const clearBtn = document.querySelector(".clear");

checkboxes.forEach(box=>{
    box.addEventListener("change",()=>{

        let checked = false;

        checkboxes.forEach(cb=>{
            if(cb.checked){
                checked = true;
            }
        });

        clearBtn.style.display = checked ? "block" : "none";
    });
});


clearBtn.addEventListener("click",(e)=>{
    e.preventDefault();

    checkboxes.forEach(cb=>{
        cb.checked = false;
    });

    clearBtn.style.display = "none";
});

// size box js


const sizeButtons = document.querySelectorAll(".size-button");
const clearBtn2 = document.querySelector(".size-clear");

sizeButtons.forEach(btn => {
    btn.addEventListener("click", function(){
        clearBtn2.style.display = "block";
    });
});
