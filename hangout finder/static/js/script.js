function initMap() {
    navigator.geolocation.getCurrentPosition(function (position) {
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        // Initialize map centered at user location
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 14,
            center: userLocation
        });

        // Add marker for user location
        new google.maps.Marker({ position: userLocation, map: map, title: "You are here!" });

        // Fetch nearby places
        const service = new google.maps.places.PlacesService(map);
        service.nearbySearch(
            {
                location: userLocation,
                radius: 5000, // 5km radius
                type: ["restaurant", "cafe", "park", "night_club", "museum"]
            },
            (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    displayPlaces(results, map);
                } else {
                    console.error("Places API Error:", status);
                }
            }
        );
    });
}

function displayPlaces(places, map) {
    const placesList = document.getElementById("places-list");
    placesList.innerHTML = ""; // Clear previous results

    places.forEach((place) => {
        // Add marker for each place
        const marker = new google.maps.Marker({
            position: place.geometry.location,
            map: map,
            title: place.name
        });

        // Append place to sidebar
        const placeElement = document.createElement("div");
        placeElement.classList.add("place-item");
        placeElement.innerHTML = `
            <h3>${place.name}</h3>
            <p>${place.vicinity}</p>
        `;
        placesList.appendChild(placeElement);

        // On click, center map on marker
        placeElement.addEventListener("click", () => {
            map.setCenter(marker.getPosition());
        });
    });
}