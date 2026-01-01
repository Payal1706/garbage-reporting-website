<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Report Garbage</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

</head>

<script>
function searchLocation() {
    let query = document.getElementById("location").value;

    if (query.length < 3) return;

    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`)
        .then(response => response.json())
        .then(data => {
            let list = document.getElementById("suggestions");
            list.innerHTML = "";

            data.forEach(place => {
                let div = document.createElement("div");
                div.style.padding = "5px";
                div.style.cursor = "pointer";
                div.innerText = place.display_name;

                div.onclick = () => {
                    document.getElementById("location").value = place.display_name;
                    list.innerHTML = "";
                };

                list.appendChild(div);
            });
        });
}
</script>




<body>

<header>
    <h1>Report Garbage</h1>
</header>

<section class="form-section">
    <h2>Submit Garbage Complaint</h2>

    <form>

        <label>Name:</label>
        <input type="text" placeholder="Enter your name" required>

        <label>Mobile Number:</label>
        <input type="text" placeholder="Enter mobile number" required>
<label>Location:</label>
<input type="text" id="location" placeholder="Type location..." onkeyup="searchLocation()">
<div id="suggestions" style="border:1px solid #ccc; max-height:150px; overflow:auto;"></div>

        <label>Garbage Type:</label>
        <select>
            <option>Plastic</option>
            <option>Wet Waste</option>
            <option>Dry Waste</option>
            <option>Other</option>
        </select>

        <label>Upload Image:</label>
        <input type="file">

        <label>Description:</label>
        <textarea placeholder="Describe the issue"></textarea>

        <button type="submit">Submit Complaint</button>
    </form>
    <a href="report.html">Report Garbage</a>
</section>


</body>
</html>
