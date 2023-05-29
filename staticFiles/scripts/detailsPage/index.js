function addLoaderListener() {
    window.addEventListener('load', function () {
        // Simulating fetching data from the backend
        // Replace this with your actual data fetching logic
        setTimeout(function () {
            // Remove the loading screen
            let loadingScreen = document.getElementById('loading-screen');
            loadingScreen.parentNode.removeChild(loadingScreen);
        }, 1000); // Simulating a 3-second delay
    });
}

async function fetchTheInitData(){

}

async function main(){
    addLoaderListener();
    await fetchTheInitData();
}

main().then(r => {});