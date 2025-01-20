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
