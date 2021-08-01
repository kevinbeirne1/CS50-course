// document.addEventListener("DOMContentLoaded", () => {
//     // Send a GET request to the url
//     fetch('https://api.exchangeratesapi.io/latest?base=USD')
//     // Put respone into a json form
//     .then(response => response.json())
//     .then(data => {
//         // Log data to the console
//         console.log(data);
//         });
// });

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = function () {
        let api_key = JSON.parse(data)[0].apiKey;
        // console.log(api_key)


        fetch(`http://api.exchangeratesapi.io/v1/latest?access_key=${api_key}&format=1`)
            // Put response into json form
            .then(response => response.json())
            .then(data => {
                // Log data to the console
                console.log(data);

                // Get currency from user input and convert to upper case
                const currency = document.querySelector('#currency').value.toUpperCase();

                const rate = data.rates[currency];
                // console.log(rate);  // Only here for troubleshooting

                // Check if currency is valid:
                if (rate !== undefined) {
                    // Display exchange on the screen
                    document.querySelector('#result').innerHTML = `1 EUR is equal to ${rate.toFixed(3)} ${currency}`;
                } else {
                    // Display error on the screen
                    document.querySelector('#result').innerHTML = "Invalid currency choice."
                }
            })
            // Catch any errors and log them to the console
            .catch(error => {
                console.log("Error:", error);
            })
        // Prevent default submission
        return false;
    }
});