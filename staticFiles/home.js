function addBtnListeners(){
    let confirmBtn = document.getElementById('confirmBtn');
    let infoBtn = document.getElementById('infoBtn');
    let cancelBtn = document.getElementById('refuseBtn');

    confirmBtn.addEventListener('click', () => {
        let acceptedCard = document.getElementsByClassName('tphoto card current')[0];
        let file_path = acceptedCard.getAttribute('file_path');
        sendDataToServer(acceptedCard.id, true, file_path);
        showCardInfo(acceptedCard.id);
        fetchData();
    });

    infoBtn.addEventListener('click', () => {
        console.log("info");
    });

    cancelBtn.addEventListener('click', () => {
        hideCardInfo();
        fetchNewCard();
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
  document.getElementById('card-name').textContent = card.name;
  document.getElementById('card-age').textContent = card.age;
  document.getElementById('card-info1').textContent = card.info1;
  document.getElementById('card-info2').textContent = card.info2;
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

function showCardInfo(cardId){
    const card = {
    name: "{{data.cards_name[0]}}", // Replace with the appropriate data from the card
    age: 27, // Replace with the appropriate data from the card
    info1: 'Information 1', // Replace with the appropriate data from the card
    info2: 'Information 2' // Replace with the appropriate data from the card
  };

  // Update the card information in the container
  updateCardInfo(card);

  setTimeout(function () {
    const cardInfo = document.querySelector('.card-info');
    cardInfo.classList.add('show');
  }, 300);
}


function fetchData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if(data.request_type === 'cardInfo')
                console.log('okay card info');
            document.getElementById('testFetch').innerText = data.time;
        })
        .catch(error => {
            console.log('Error fetching data:', error);
        });
}

function fetchNewCard() {
    fetch('/api/getNewCard')
        .then(response => response.json())
        .then(data => {
            if(data.request_type === 'newCard'){
                let container = document.getElementById('card-container');
                container.insertAdjacentHTML('beforeend', data.content);
                animateCard();
            }
        })
        .catch(error => {
            console.log('Error fetching data:', error);
        });
}

function sendDataToServer(cardId, accepted, file_path) {
  // Create the data object to send
  const data = {
    card_id: cardId,
    accepted: accepted,
    file_path: file_path
  };

  // Send the data to the server using fetch API
  fetch('/details-card', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => {
      if (response.ok) {
        console.log('Data sent successfully');
      } else {
        console.error('Failed to send data');
      }
    })
    .catch(error => {
      console.error('Error occurred while sending data:', error);
    });
}

function main(){
    fetchData();
    addBtnListeners();
    animateCard();
}

main();