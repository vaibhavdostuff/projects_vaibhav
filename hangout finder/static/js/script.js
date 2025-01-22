let service, userLocation;

function initMap() {
    navigator.geolocation.getCurrentPosition(function (position) {
        userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        // Initialize map centered at user's current location
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 14,
            center: userLocation
        });

        // Add marker for user location
        new google.maps.Marker({ 
            position: userLocation, 
            map: map, 
            title: "You are here!" 
        });

        // Initialize Google Places service
        service = new google.maps.places.PlacesService(map);

        // Fetch initial places (default: restaurant)
        fetchPlaces("restaurant");
    });
}

function fetchPlaces(type) {
    service.nearbySearch(
        {
            location: userLocation,
            radius: 5000,  // Search within 5km
            type: [type]   // Dynamically fetch places based on selected type
        },
        (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
                displayPlaces(results);
            } else {
                console.error("Places API Error:", status);
            }
        }
    );
}

function displayPlaces(places) {
    const placesList = document.getElementById("places");
    placesList.innerHTML = ""; // Clear previous results

    places.forEach((place) => {
        // Add marker for each place
        const marker = new google.maps.Marker({
            position: place.geometry.location,
            map: map,
            title: place.name
        });

        // Append place to the sidebar
        const placeElement = document.createElement("div");
        placeElement.classList.add("place-item");
        placeElement.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.vicinity}</p>
        `;
        placesList.appendChild(placeElement);

        // On click, center the map on the selected place marker
        placeElement.addEventListener("click", () => {
            map.setCenter(marker.getPosition());
        });
    });
}

function filterPlaces() {
    const selectedType = document.getElementById("place-type").value;
    fetchPlaces(selectedType);
}
