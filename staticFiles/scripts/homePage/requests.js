
async function sendDataToServer(cardId, file_path, image_path) {
  // Create the data object to send
  const data = {
    card_id: cardId,
    file_path: file_path,
    image_path: image_path
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

async function fetchNewCard() {
    const result = await fetch('/api/getNewCard');
    try{
        const data = await result.json();
        console.log(data);
        if(data.request_type === 'newCard'){
            console.log("test");
            let container = document.getElementById('card-container');
            container.insertAdjacentHTML('beforeend', data.content);
        }
    }catch(error){
        console.log('Error fetching data:', error);
    }
}

async function calculateSuggestions(card_file_path) {

    const data = {
      card_path: card_file_path
    };

    const result = await fetch('/api/setSuggestions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    try{
      if(result.ok){
         console.log('Data sent successfully');
      }else{
          console.error('Failed to send data');
      }
    }catch(error){
        console.error('Error occurred while sending data:', error);
    }
}