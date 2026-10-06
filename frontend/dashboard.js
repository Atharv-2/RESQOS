/* ---------- Icons (inline SVG paths) ---------- */
const ICONS = {
  shield:'<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
  search:'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
  pin:'<path d="M12 21s-6-5.4-6-10a6 6 0 0 1 12 0c0 4.6-6 10-6 10z"/><circle cx="12" cy="11" r="2"/>',
  temp:'<path d="M10 14.5V5a2 2 0 1 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
  rain:'<path d="M7 15a4 4 0 1 1 1-7.9A5 5 0 0 1 17.5 9 3.5 3.5 0 0 1 17 16H7z"/><path d="M8 19l-1 2M12 19l-1 2M16 19l-1 2"/>',
  drop:'<path d="M12 3s6 6.2 6 10.5a6 6 0 0 1-12 0C6 9.2 12 3 12 3z"/><path d="M9.5 14a2.5 2.5 0 0 0 2.5 2.5"/>',
  cloud:'<path d="M7 18a4 4 0 1 1 1-7.9A5 5 0 0 1 17.5 12 3 3 0 0 1 17 18H7z"/>',
  map:'<path d="M9 4L3 6.5v13L9 17l6 3 6-2.5v-13L15 7z"/><path d="M9 4v13M15 7v13"/>',
  info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
  hospital:'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/>',
  police:'<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M12 8.5l1.1 2.3 2.5.3-1.8 1.7.5 2.5-2.3-1.2-2.3 1.2.5-2.5-1.8-1.7 2.5-.3z"/>',
  building:'<path d="M4 21V8l8-5 8 5v13M9 21v-6h6v6"/>',
  alert:'<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/>',
  river:'<path d="M3 8c3-2 5 2 9 0s6 2 9 0M3 13c3-2 5 2 9 0s6 2 9 0M3 18c3-2 5 2 9 0s6 2 9 0"/>'
};
const icon = n => `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICONS[n] || ''}</svg>`;
document.querySelectorAll('[data-icon]').forEach(el => { el.innerHTML = icon(el.dataset.icon); });

/* ---------- Location search (frontend only) ---------- */
const form = document.getElementById('search-form');
const input = document.getElementById('location-input');
const nameEl = document.getElementById('location-name');
const mapEl = document.getElementById('map-location');
const msg = document.getElementById('search-msg');
const temperatureEl = document.getElementById('temperature');
const rainfallEl = document.getElementById('rainfall');
const humidityEl = document.getElementById('humidity');
const weatherConditionEl =
    document.getElementById('weather-condition');
function getWeatherCondition(code) {

    if (code === 0) return "Clear Sky";

    if (code === 1) return "Mainly Clear";

    if (code === 2) return "Partly Cloudy";

    if (code === 3) return "Overcast";

    if (code === 45 || code === 48)
        return "Fog";

    if (code >= 51 && code <= 57)
        return "Drizzle";

    if (code >= 61 && code <= 67)
        return "Rain";

    if (code >= 71 && code <= 77)
        return "Snow";

    if (code >= 80 && code <= 82)
        return "Rain Showers";

    if (code >= 85 && code <= 86)
        return "Snow Showers";

    if (code >= 95)
        return "Thunderstorm";

    return "Unknown";
}
form.addEventListener('submit', async (e) => {

    e.preventDefault();

    const location = input.value.trim();

    if (!location) {
        msg.textContent = 'Please enter a location.';
        msg.classList.add('error');
        return;
    }

    msg.classList.remove('error');
    msg.textContent = 'Searching location...';

    try {

        const geoURL =
            `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(location)}&count=1&language=en&format=json`;

        const geoResponse = await fetch(geoURL);
        const geoData = await geoResponse.json();

        if (!geoData.results || geoData.results.length === 0) {
            msg.textContent = 'Location not found.';
            msg.classList.add('error');
            return;
        }

        const place = geoData.results[0];

        const latitude = place.latitude;
        const longitude = place.longitude;

        console.log("Location:", place.name);
        console.log("Latitude:", latitude);
        console.log("Longitude:", longitude);
        // STEP 2: Get real weather data

const weatherURL =
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,rain,weather_code`;

const weatherResponse = await fetch(weatherURL);

const weatherData = await weatherResponse.json();
console.log("Weather Data:", weatherData);
const currentWeather = weatherData.current;

temperatureEl.textContent =
    currentWeather.temperature_2m + "°C";

rainfallEl.textContent =
    currentWeather.rain + " mm";

humidityEl.textContent =
    currentWeather.relative_humidity_2m + "%";
weatherConditionEl.textContent =
    getWeatherCondition(currentWeather.weather_code);
    // Update location on dashboard
nameEl.textContent = place.name;
mapEl.textContent = place.name;

msg.textContent = "Real weather data loaded successfully.";


    } catch (error) {

        console.error(error);

        msg.textContent = 'Unable to fetch location data.';
        msg.classList.add('error');

    }

});

input.addEventListener('input', () => {
  if (msg.classList.contains('error')) { msg.textContent = ''; msg.classList.remove('error'); }
});