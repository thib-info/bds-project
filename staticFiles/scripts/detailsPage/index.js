function addLoaderListener() {
    window.addEventListener('load', function () {
        setTimeout(function () {
            let loadingScreen = document.getElementById('loading-screen');
            loadingScreen.parentNode.removeChild(loadingScreen);
        }, 1000); // Simulating a 3-second delay
    });
}

async function fetchTheInitData(){
    await getDetails();
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