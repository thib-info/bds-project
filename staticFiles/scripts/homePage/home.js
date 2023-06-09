
function addBtnListeners(){
    let confirmBtn = document.getElementById('confirmBtn');
    let infoBtn = document.getElementById('infoBtn');
    let cancelBtn = document.getElementById('refuseBtn');

    infoBtn.addEventListener('click', async () => {
        let acceptedCard = document.getElementsByClassName('tphoto card current')[0];
        let file_path = acceptedCard.getAttribute('file_path');
        let image_path = acceptedCard.getAttribute('style').split('url(')[1].split(')')[0];
        await sendDataToServer(acceptedCard.id, file_path, image_path);
        calculateSuggestions(file_path).then(r => {});
        activateSelect();
    });

    confirmBtn.addEventListener('click', () => {
        window.location.href = "/selectedCard";
    });

    cancelBtn.addEventListener('click', async() => {
        disableSelect();
        hideCardInfo();
        await fetchNewCard();
        animateCard();
    });

}

function activateSelect(){
    let confirmBtn = document.getElementById('confirmBtn');
    confirmBtn.classList.remove('hidden');
}

function disableSelect(){
    let confirmBtn = document.getElementById('confirmBtn');
    confirmBtn.classList.add('hidden');
}

function animateCard(){
    const cards = Array.from(document.getElementsByClassName('tphoto card'));

    cards.forEach(function(card) {
        document.getElementById('infoBtn').addEventListener('click', () => {
            const currentCard = card;
            if(!card.classList.contains('hidden')) {
                getNextCard(currentCard);
                currentCard.classList.add('accepted');
            }
        });
    });

    document.getElementById('refuseBtn').addEventListener('click', function() {
      const currentCard = document.querySelector('.tphoto.card:not(.hidden)');
      const nextCard = getNextCard(currentCard);

      currentCard.classList.add('rejected');

      setTimeout(function() {
        currentCard.remove();
        nextCard.classList.remove('hidden');
        nextCard.classList.add('current');
      }, 500);
    });
}

function getNextCard(currentCard) {
  const cardContainer = currentCard.parentNode;
  const cards = Array.from(cardContainer.getElementsByClassName('tphoto'));

  const currentIndex = cards.indexOf(currentCard);
  const nextIndex = (currentIndex + 1) % cards.length;

  return cards[nextIndex];
}

// Update the card information based on the selected card
function updateCardInfo(card) {
    const container = document .getElementById('card-info-details');
    container.innerHTML = "";
    Object.keys(card).forEach((element) => {
        const paragraph = document.createElement('p');
        paragraph.textContent = element + ": " + card[element];
        container.insertBefore(paragraph, container.firstChild);
  });
}

function hideCardInfo(){
    const cardElement = document.querySelector('.tphoto.card');
  const cardInfo = document.querySelector('.card-info');

  if (cardInfo.classList.contains('show')) {
    cardInfo.classList.remove('show');

    setTimeout(function () {
      cardElement.classList.remove('accepted');
    }, 300);
  } else {
    cardElement.classList.remove('accepted');
  }
}

function showCardInfo(details){
  updateCardInfo(details);

  setTimeout(function () {
    const cardInfo = document.querySelector('.card-info');
    cardInfo.classList.add('show');
  }, 300);
}

function main(){
    addBtnListeners();
    animateCard();
}

main();