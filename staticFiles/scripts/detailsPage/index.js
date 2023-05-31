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
    await getSuggestions()
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

async function main(){
    addLoaderListener();
    await fetchTheInitData();
}

main().then(r => {});