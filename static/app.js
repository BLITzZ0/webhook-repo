function formatTimestamp(iso) {
  const date = new Date(iso);
  const day = date.getUTCDate();
  const month = date.toLocaleString('en-US', { month: 'long', timeZone: 'UTC' });
  const year = date.getUTCFullYear();
  const hours = date.getUTCHours();
  const minutes = date.getUTCMinutes().toString().padStart(2, '0');
  const suffix = hours >= 12 ? 'PM' : 'AM';
  const hour12 = hours % 12 === 0 ? 12 : hours % 12;

  const ordinal = (d) => {
    if (d > 3 && d < 21) return 'th';
    switch (d % 10) {
      case 1: return 'st';
      case 2: return 'nd';
      case 3: return 'rd';
      default: return 'th';
    }
  };

  return `${day}${ordinal(day)} ${month} ${year} - ${hour12}:${minutes} ${suffix} UTC`;
}

async function fetchEvents() {
  try {
    const res = await fetch('/api/events');
    const events = await res.json();
    const container = document.getElementById('events');
    container.innerHTML = '';

    events
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .forEach(event => {
        const div = document.createElement('div');
        div.className = 'event';

        const { author, from_branch, to_branch, action, timestamp } = event;
        const formattedTime = formatTimestamp(timestamp);

        let content = '';

        if (action === 'PUSH') {
          content = `"${author}" pushed to "${to_branch}" on ${formattedTime}`;
        } else if (action === 'PULL_REQUEST') {
          content = `"${author}" submitted a pull request from "${from_branch}" to "${to_branch}" on ${formattedTime}`;
        } else if (action === 'MERGE') {
          content = `"${author}" merged branch "${from_branch}" to "${to_branch}" on ${formattedTime}`;
        } else {
          content = 'Unknown event type';
        }

        div.textContent = content;
        container.appendChild(div);
      });
  } catch (err) {
    console.error('Error fetching events:', err);
    document.getElementById('events').textContent = 'Failed to load events.';
  }
}

fetchEvents();
setInterval(fetchEvents, 15000); // Refresh every 15 seconds
