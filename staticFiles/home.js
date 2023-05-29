function addBtnListeners(){
    let confirmBtn = document.getElementById('confirmBtn');
    let infoBtn = document.getElementById('infoBtn');
    let cancelBtn = document.getElementById('refuseBtn');

    confirmBtn.addEventListener('click', async () => {
        let acceptedCard = document.getElementsByClassName('tphoto card current')[0];
        let file_path = acceptedCard.getAttribute('file_path');
        await sendDataToServer(acceptedCard.id, file_path);
    });

    infoBtn.addEventListener('click', () => {
        console.log("info");
    });

    cancelBtn.addEventListener('click', () => {
        hideCardInfo();
    });
}

function animateCard(){
    const cards = Array.from(document.getElementsByClassName('tphoto card'));

    cards.forEach(function(card) {
        document.getElementById('confirmBtn').addEventListener('click', () => {
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
        currentCard.classList.add('hidden');
        currentCard.classList.remove('current');
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
        paragraph.textContent = element + " : " + card[element];
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


async function fetchData() {
    const result = await fetch('/api/data')
    try{
        const data = await result.json();
        console.log(data);
    }catch (error){
        console.log('Error fetching data:', error);
    }

}

async function sendDataToServer(cardId, file_path) {
  // Create the data object to send
  const data = {
    card_id: cardId,
    file_path: file_path
  };

  // Send the data to the server using fetch API
  const result = await fetch('/details-card', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  try{
      if(result.ok){
         console.log('Data sent successfully');
         const data = await result.json();
         showCardInfo(data.content);
      }else{
          console.error('Failed to send data');
      }
  }catch(error){
      console.error('Error occurred while sending data:', error);
  }
}

function main(){
    addBtnListeners();
    animateCard();
}

main();