async function fetchInfo(file_path, image_path) {
  const data = {
    file_path: file_path,
    image_path: image_path
  };

  const result = await fetch('/details-card', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });

  try{
      if(result.ok){
          return await result.json();
      }else{
          console.error('Failed to send data');
          return null;
      }
  }catch(error){
      console.error('Error occurred while sending data:', error);
      return null;
  }
}

async function fetchSuggestions(){
    const result = await fetch('/api/data')
    try{
        const data = await result.json();
        console.log(data);
        return data.select_card_mapping;
    }catch (error){
        console.log('Error fetching data:', error);
        return null;
    }
}

async function fetchReco(){
    const result = await fetch('/api/data')
    try{
        const data = await result.json();
        console.log(data);
        console.log('test');
        return data.cards_reco;
    }catch (error){
        console.log('Error fetching data:', error);
        return null;
    }
}