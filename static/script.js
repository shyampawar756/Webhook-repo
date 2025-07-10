function fetchEvents() {
    fetch("/data")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("events");
            list.innerHTML = ""; // Clear existing list
            data.forEach(event => {
                let message = "";
                if (event.action === "push") {
                    message = `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
                } else if (event.action === "pull_request") {
                    message = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
                } else if (event.action === "merge") {
                    message = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
                }
                const li = document.createElement("li");
                li.innerText = message;
                list.appendChild(li);
            });
        });
}

fetchEvents(); // Run once on load
setInterval(fetchEvents, 15000); // Refresh every 15 seconds
