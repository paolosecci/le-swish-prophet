// Constants
const teams = ["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"];

const fullNames = {
  "ATL": "Atlanta Hawks", "BKN": "Brooklyn Nets", "BOS": "Boston Celtics", "CHA": "Charlotte Hornets",
  "CHI": "Chicago Bulls", "CLE": "Cleveland Cavaliers", "DAL": "Dallas Mavericks", "DEN": "Denver Nuggets",
  "DET": "Detroit Pistons", "GSW": "Golden State Warriors", "HOU": "Houston Rockets", "IND": "Indiana Pacers",
  "LAC": "Los Angeles Clippers", "LAL": "Los Angeles Lakers", "MEM": "Memphis Grizzlies", "MIA": "Miami Heat",
  "MIL": "Milwaukee Bucks", "MIN": "Minnesota Timberwolves", "NOP": "New Orleans Pelicans", "NYK": "New York Knicks",
  "OKC": "Oklahoma City Thunder", "ORL": "Orlando Magic", "PHI": "Philadelphia 76ers", "PHX": "Phoenix Suns",
  "POR": "Portland Trail Blazers", "SAC": "Sacramento Kings", "SAS": "San Antonio Spurs", "TOR": "Toronto Raptors",
  "UTA": "Utah Jazz", "WAS": "Washington Wizards"
};

// DOM elements
const select1 = document.getElementById("selDataset");
const select2 = document.getElementById("selDataset2");
const updateBtn = document.getElementById("update-btn");
const calcBtn = document.getElementById("calc");
const lastUpdateEl = document.getElementById("last-update");

// Populate team selects
teams.forEach(team => {
  const opt = document.createElement("option");
  opt.value = team;
  opt.textContent = team;
  select1.appendChild(opt.cloneNode(true));
  select2.appendChild(opt);
});

// Load last-update info
document.addEventListener('DOMContentLoaded', async () => {
  console.log("DOMContentLoaded fired - fetching last update");
  try {
    const res = await fetch("/last-update");
    console.log("Fetch status:", res.status, "OK:", res.ok);
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    const data = await res.json();
    console.log("Data received:", data);
    document.getElementById("last-update").textContent = data.last_update || "Never";

    // Handle last-update info displayed and update-button availability
    const lastUpdate = data.last_update;
    if (lastUpdate === "Never") {
      document.getElementById("last-update").textContent = "Never";
      document.getElementById("update-btn").style.display = "inline-block"; // show button
    } else {
      const lastDate = new Date(lastUpdate).toLocaleDateString('en-US', { timeZone: 'America/Los_Angeles' });
      const today = new Date().toLocaleDateString('en-US', { timeZone: 'America/Los_Angeles' });
      
      if (lastDate === today) {
        document.getElementById("last-update").textContent = "Today";
        document.getElementById("update-btn").style.display = "none"; // hide button
      } else {
        document.getElementById("last-update").textContent = lastDate;
        document.getElementById("update-btn").style.display = "inline-block"; // show button
      }
    }
  } catch (err) {
    console.error("Last update fetch error:", err);
    document.getElementById("last-update").textContent = "Error loading timestamp";
    document.getElementById("update-btn").style.display = "block";
  }
});

// Refresh NBA data (keep as is, but add hide after success)
updateBtn.addEventListener("click", async () => {
  try {
    document.getElementById("update-btn").textContent = "Hacking into NBA databases...<br>(exp. 1-2 minutes)";
    const res = await fetch("/update");
    const data = await res.json();
    lastUpdateEl.textContent = "Today";
    updateBtn.style.display = "none"; // hide after update
    alert("NBA Data Mining Operation: SUCCESS");
  } catch (err) {
    console.error("Update failed:", err);
    alert("Failed to update data. Check console for error info.");
  }
});

// Team 1 selection
select1.addEventListener("change", async (e) => {
  const team = e.target.value;
  if (!team) return;

  try {
    const res = await fetch(`/predict/${team}`);
    const data = await res.json();

    document.getElementById("team-lineup-header").innerHTML = "Predicted Lineup:";
    document.getElementById("player-name").innerHTML = data[1].map(p => `
      <div class="grid grid-cols-5 gap-4 bg-[#111111]/80 p-4 rounded-lg border border-[#222222]">
        <span class="font-semibold text-[#dddddd] col-span-2">${p.NAME}</span>
        <span class="text-[#dddddd] text-center">P: ${p.PTS}</span>
        <span class="text-[#dddddd] text-center">R: ${p.REB}</span>
        <span class="text-[#dddddd] text-center">A: ${p.AST}</span>
      </div>
    `).join('');
    document.getElementById("team-data").innerHTML = "<h6>Waiting for opponent...</h6>";
  } catch (err) {
    console.error("Team 1 fetch failed:", err);
  }
});

// Team 2 selection
select2.addEventListener("change", async (e) => {
  const team = e.target.value;
  if (!team) return;

  try {
    const res = await fetch(`/predict/${team}`);
    const data = await res.json();

    document.getElementById("team-lineup-header2").innerHTML = "Predicted Lineup:";
    document.getElementById("player-name2").innerHTML = data[1].map(p => `
      <div class="grid grid-cols-5 gap-4 bg-[#111111]/80 p-4 rounded-lg border border-[#222222]">
        <span class="font-semibold text-[#dddddd] col-span-2">${p.NAME}</span>
        <span class="text-[#dddddd] text-center">P: ${p.PTS}</span>
        <span class="text-[#dddddd] text-center">R: ${p.REB}</span>
        <span class="text-[#dddddd] text-center">A: ${p.AST}</span>
      </div>
    `).join('');
    document.getElementById("team-data2").innerHTML = "<h6>Building matchups...</h6>";
  } catch (err) {
    console.error("Team 2 fetch failed:", err);
  }
});

// Calculate winner
calcBtn.addEventListener("click", async () => {
  const t1 = select1.value;
  const t2 = select2.value;
  if (!t1 || !t2) return alert("Select both teams");

  try {
    const res = await fetch(`/simgame/${t1}/${t2}`);
    const [t1s, t2s] = await res.json();

    document.getElementById("team-data").innerHTML = `<h1>${Math.round(t1s)}</h1>`;
    document.getElementById("team-data2").innerHTML = `<h1>${Math.round(t2s)}</h1>`;

    const winner = t1s > t2s ? t1 : t2;
    document.getElementById("winningteam").innerHTML = `
      <img src="/static/img/logos/${winner}_logo.svg" width="250" height="250" alt="${fullNames[winner]}" class="mx-auto" />
      <h1 class="text-4xl font-bold text-[#dddddd] mt-4">${fullNames[winner]}</h1>
    `;

    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
  } catch (err) {
    console.error("Sim game failed:", err);
    alert("Failed to calculate winner. Try again.");
  }
});