/* ======================================
   TrafficEye JavaScript
====================================== */

document.addEventListener("DOMContentLoaded", function () {

    // ===============================
    // Auto Hide Alerts
    // ===============================

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function(alert){

        setTimeout(function(){

            alert.style.transition = "0.5s";

            alert.style.opacity = "0";

            setTimeout(function(){

                alert.remove();

            },500);

        },3000);

    });

    // ===============================
    // Delete Confirmation
    // ===============================

    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function(button){

        button.addEventListener("click",function(e){

            const confirmDelete = confirm(
                "Are you sure you want to delete this record?"
            );

            if(!confirmDelete){

                e.preventDefault();

            }

        });

    });

    // ===============================
    // Form Validation
    // ===============================

    const forms = document.querySelectorAll("form");

    forms.forEach(function(form){

        form.addEventListener("submit",function(e){

            const requiredFields = form.querySelectorAll("[required]");

            let valid = true;

            requiredFields.forEach(function(field){

                if(field.value.trim() === ""){

                    field.classList.add("is-invalid");

                    valid = false;

                }else{

                    field.classList.remove("is-invalid");

                }

            });

            if(!valid){

                e.preventDefault();

            }

        });

    });

    // ===============================
    // Search Input
    // ===============================

    const searchInput = document.querySelector("input[name='search']");

    if(searchInput){

        searchInput.addEventListener("keyup",function(){

            this.style.borderColor = "#0d6efd";

        });

    }

    // ===============================
    // Back To Top
    // ===============================

    const topButton = document.getElementById("backToTop");

    window.addEventListener("scroll",function(){

        if(topButton){

            if(window.scrollY > 200){

                topButton.style.display = "block";

            }else{

                topButton.style.display = "none";

            }

        }

    });

    if(topButton){

        topButton.addEventListener("click",function(){

            window.scrollTo({

                top:0,

                behavior:"smooth"

            });

        });

    }

    // ===============================
    // Loading Button
    // ===============================

    const submitButtons = document.querySelectorAll("button[type='submit']");

    submitButtons.forEach(function(button){

        button.addEventListener("click",function(){

            button.disabled = true;

            button.innerHTML =

            '<span class="spinner-border spinner-border-sm"></span> Processing...';

            button.form.submit();

        });

    });

});