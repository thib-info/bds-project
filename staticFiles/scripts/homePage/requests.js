
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