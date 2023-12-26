document.addEventListener('DOMContentLoaded', function() {
    const reviews = document.querySelectorAll('.review');

    reviews.forEach(review => {
        const rating = review.getAttribute('data-rating');
        let starsHtml = '';

        for (let i = 0; i < rating; i++) {
            starsHtml += '<i class="bi bi-star-fill text-warning"></i>'; // étoiles en jaune
        }

        for (let i = rating; i < 5; i++) {
            starsHtml += '<i class="bi bi-star text-secondary"></i>'; // étoiles non remplies
        }

        review.innerHTML = starsHtml;
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.rating .bi-star');
    const ratingInput = document.getElementById('ratingInput');

    stars.forEach(star => {
        star.addEventListener('mouseover', function() {
            fillStarsUpTo(this.getAttribute('data-rating'));
        });

        star.addEventListener('click', function() {
            ratingInput.value = this.getAttribute('data-rating');
            fillStarsUpTo(this.getAttribute('data-rating')); // Remplir les étoiles lors du clic
        });

        star.addEventListener('mouseout', function() {
            fillStarsUpTo(ratingInput.value || 0);
        });
    });

    function fillStarsUpTo(rating) {
        stars.forEach(star => {
            if (star.getAttribute('data-rating') <= rating) {
                star.classList.add('bi-star-fill', 'text-warning'); // Remplir et colorer l'étoile
                star.classList.remove('bi-star');
            } else {
                star.classList.add('bi-star', 'text-secondary'); // Étoile non remplie
                star.classList.remove('bi-star-fill', 'text-warning');
            }
        });
    }
});

