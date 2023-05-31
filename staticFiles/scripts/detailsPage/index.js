let map;
let data;
let init_coordinates = {lat: 0, lon: 0};
let markers = {};

function getImgPath(){
    let img = document.getElementById('object-selected-image');
    return img.getAttribute('src');
}

function getFilePath(){
    let img = document.getElementById('object-selected-image');
    return img.getAttribute('file_path');
}

function addLoaderListener() {
    window.addEventListener('load', function () {
        setTimeout(function () {
            let loadingScreen = document.getElementById('loading-screen');
            loadingScreen.parentNode.removeChild(loadingScreen);
        }, 1000);
    });
}

async function fetchTheInitData(){
    await getDetails();
    // await getSuggestions()
}

async function getSuggestions(){
    const dict_suggestions = await fetchSuggestions();
    const file_path = getFilePath();
    const suggestions_paths = dict_suggestions[file_path]['files_path'];
    const suggestions_img = dict_suggestions[file_path]['images_path'];

    addSuggestionCard(suggestions_img);
    addArrowListener();

}

function addArrowListener(){
    const cardsContainer = document.querySelector('.cards-container');
    const sliderArrow = document.querySelector('.slider-arrow');

    sliderArrow.addEventListener('click', () => {
      const cardWidth = cardsContainer.firstElementChild.offsetWidth;
      cardsContainer.style.transform = `translateX(-${cardWidth}px)`;
      cardsContainer.appendChild(cardsContainer.firstElementChild);
    });
}

function addSuggestionCard(suggestedCards){
    const cardsContainer = document.querySelector('.cards-container');

    suggestedCards.forEach((cardData) => {
      const cardElement = document.createElement('div');
      cardElement.classList.add('card-suggest');
      cardElement.style.backgroundImage = `url(${cardData})`;
      cardsContainer.appendChild(cardElement);
    });
}

async function getDetails() {
  let img = document.getElementById('object-selected-image');
  let file_path = img.getAttribute('file_path');
  const details = (await fetchInfo(file_path, img.getAttribute('src'))).content;

  const container = document.getElementsByClassName('container-details')[0];
  container.innerHTML = "";

  if (details !== null) {
    const card = document.createElement('div');
    card.classList.add('card');

    const columnsWrapper = document.createElement('div');
    columnsWrapper.classList.add('columns-wrapper');

    const leftColumn = document.createElement('div');
    leftColumn.classList.add('column');

    const rightColumn = document.createElement('div');
    rightColumn.classList.add('column');

    Object.keys(details).forEach((element) => {
      if (element === 'Beschrijving') {
        const descriptionParagraph = document.createElement('p');
        descriptionParagraph.classList.add('full-width');
        descriptionParagraph.textContent = 'Beschrijving: ' + details[element];
        card.appendChild(descriptionParagraph);
      } else {
        const paragraph = document.createElement('p');
        paragraph.textContent = element + ": " + details[element];

        if (leftColumn.childElementCount <= rightColumn.childElementCount) {
          leftColumn.appendChild(paragraph);
        } else {
          rightColumn.appendChild(paragraph);
        }
      }
    });

    columnsWrapper.appendChild(leftColumn);
    columnsWrapper.appendChild(rightColumn);
    card.appendChild(columnsWrapper);

    container.appendChild(card);
  }
}

function addPlacesListeners(){
    const selectableItems = document.querySelectorAll('.selectable-item');

    selectableItems.forEach((item) => {
      item.addEventListener('click', () => {
        item.classList.toggle('selected');

        if (item.classList.contains('selected')) {
            addPlaceToMap(item);
          console.log('Selected:', item.textContent);
        } else {
            removeMarker(item);
          console.log('Deselected:', item.textContent);
        }
      });
    });
}

function addPlaces(data) {
  const container = document.querySelector('.selectable-items');
  let index = 0;
  data.forEach(item => {
    const amenity = item['Amenity'][0];
    const name = item['Name'][0];
    const coordinates = item['Coordinates'];
    const address = item['Address'];

    const selectableItem = document.createElement('div');
    selectableItem.classList.add('selectable-item');
    selectableItem.setAttribute('index', index);

    const typeElement = document.createElement('span');
    typeElement.textContent = amenity;
    typeElement.classList.add('type');

    const nameElement = document.createElement('span');
    nameElement.textContent = name;
    nameElement.classList.add('name');

    const locationElement = document.createElement('span');
    locationElement.textContent = address;
    locationElement.classList.add('location');

    selectableItem.appendChild(nameElement);
    selectableItem.appendChild(typeElement);
    selectableItem.appendChild(locationElement);

    container.appendChild(selectableItem);
    index += 1;
  });
}

function initMap() {
    getInitCoordinates();
    const mapOptions = {
      center: { lat: init_coordinates.lat, lng: init_coordinates.lon },
      zoom: 17
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions );
}

function getRandomHexColor() {
  // Generate random RGB values
  const red = Math.floor(Math.random() * 256);
  const green = Math.floor(Math.random() * 256);
  const blue = Math.floor(Math.random() * 256);

  // Convert RGB to hexadecimal format
    return `#${red.toString(16)}${green.toString(16)}${blue.toString(16)}`;
}

function removeMarker(item){
    const index = item.getAttribute('index');
    const place = data[index];

    if(markers.hasOwnProperty(place.Name)){
        marker = markers[place.Name];
        marker.setMap(null);
    }
}


function addPlaceToMap(item) {
  const index = item.getAttribute('index');
  const place = data[index];
  const coordinates = place['Coordinates'];
  const position = { lat: parseFloat(coordinates.latitude), lng: parseFloat(coordinates.longitude) };
  const customData = {};
  const color = getRandomHexColor();

  Object.keys(place).forEach((key) => {
    if(Array.isArray(place[key]) === true)
        customData[key] = place[key];
  });

  let marker = new google.maps.Marker({
      position,
      map,
      title: place.Name[0],
      label: {
        text: place.Name[0][0],
        color: '#000000',
      },
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        scale: 20,
        fillColor: color,
        fillOpacity: 1,
        strokeWeight: 2,
        strokeColor: "#ffffff",
      },
      customData
  });

  markers[place.Name] = marker;

    const infoWindow = new google.maps.InfoWindow();
    marker.addListener('click', function() {
      let content = `<div> <h1>${marker.customData['Name']}</h1>`;
      Object.keys(marker.customData).forEach((key) => {
          if(key !== "Name")
            content += `<p>${key}: ${marker.customData[key]}</p>`;
      });
      content += '</div>';

      // Set the info window content
      infoWindow.setContent(content);

      // Open the info window
      infoWindow.open(map, marker);
    });
}

function getMuseum(){
    let img = getImgPath();
    return img.split('/')[3];
}

function getInitCoordinates(){
    let museum = getMuseum();
    if(museum === 'alijn'){
        init_coordinates = {lat: 51.05755362299733, lon: 3.723522739298267};
    }else if(museum === 'archief'){
        init_coordinates = {lat: 51.04584607079588, lon: 3.7505423487840495};
    }else if(museum === 'design'){
        init_coordinates = {lat: 51.05590007151709, lon: 3.719668184088063};
    }else if(museum === 'industrie'){
        init_coordinates = {lat: 51.059572076526635, lon: 3.729351512923772};
    }else if(museum === 'stam'){
        init_coordinates = {lat: 51.04408963545599, lon: 3.7175096975808697};
    }
}

async function main(){
    let museum = getMuseum();
    let sample = [ {'Amenity': ['pub'], 'Name': ['The Celtic Towers'], 'Address': 'Sint-Michielshelling 5/6, 9000 Gent', 'Coordinates': {'latitude': 51.0537928, 'longitude': 3.721227}},

{'Amenity': ['cinema'], 'Name': ['Sphinx'], 'Address': 'Sint-Michielshelling 7, 9000 Gent', 'Coordinates': {'latitude': 51.0537291, 'longitude': 3.7215956}, 'Phone number': ['+32 9 225 60 86'], 'Website': ['https://www.sphinx-cinema.be/'], 'Wheelchair': ['no'], 'Payment': ['yes']} ];

    addLoaderListener();
    await fetchTheInitData();
    const reco = (await fetchReco())[museum];
    data = reco;
    addPlaces(reco);
    addPlacesListeners();
}

main().then(r => {});