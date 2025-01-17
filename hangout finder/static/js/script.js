function initMap() {
    navigator.geolocation.getCurrentPosition(function(position) {
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        const map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: userLocation
        });
        new google.maps.Marker({ position: userLocation, map: map });
    });
}
