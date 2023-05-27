function addBtnListeners(){
    const cards = Array.from(document.getElementsByClassName('tphoto card'));
    let confirmBtn = document.getElementById('confirmBtn');
    let infoBtn = document.getElementById('infoBtn');
    let cancelBtn = document.getElementById('refuseBtn');

    confirmBtn.addEventListener('click', () => {
        console.log("confirm");
    });

    infoBtn.addEventListener('click', () => {
        console.log("info");
    });

    cancelBtn.addEventListener('click', () => {
        console.log("cancel");
    });
}

function animateCard(){
    // Retrieve all the card elements
    const cards = Array.from(document.getElementsByClassName('tphoto card'));

    // Add accept event to each card
    cards.forEach(function(card) {
        document.getElementById('confirmBtn').addEventListener('click', () => {
            const currentCard = card;
            if(!card.classList.contains('hidden')) {
                const nextCard = getNextCard(currentCard);

                currentCard.classList.add('accepted');


            }
        });
    });

    document.getElementById('refuseBtn').addEventListener('click', function() {
      const currentCard = document.querySelector('.tphoto.card:not(.hidden)');
      const nextCard = getNextCard(currentCard);

      currentCard.classList.add('rejected');

      setTimeout(function() {
        currentCard.classList.add('hidden');
        nextCard.classList.remove('hidden');
      }, 500); // Adjust the delay to match the animation duration
    });
}

function getNextCard(currentCard) {
  const cardContainer = currentCard.parentNode;
  const cards = Array.from(cardContainer.getElementsByClassName('tphoto'));

  const currentIndex = cards.indexOf(currentCard);
  const nextIndex = (currentIndex + 1) % cards.length;

  return cards[nextIndex];
}

function main(){
    addBtnListeners();
    animateCard();
}

main();