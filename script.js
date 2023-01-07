const form = document.querySelector('#tool-form');
const output = document.querySelector('#output');
const usageElement = document.querySelector('#usage');
const ipAddressElement = document.querySelector('#ip-address');
const networkElement = document.querySelector('#network');
const adapterSelect = document.querySelector('#adapter-select');
const terminalOutput = document.querySelector('#terminal-output');
const terminalInput = document.querySelector('#terminal-input');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const tool = document.querySelector('#tool-select').value;
  const adapter = adapterSelect.value;
  output.innerHTML = `Running ${tool} on adapter ${adapter}...`;
  // Send a request to the backend to run the selected tool
});

terminalInput.addEventListener('submit', (event) => {
  event.preventDefault();
  const command = document.querySelector('#command-input').value;
  // Send a request to the backend to execute the command in the terminal
});

// Get technical information and display it in the page
fetch('/technical-info')
  .then((response) => response.json())
  .then((data) => {
    usageElement.textContent = data.usage;
    ipAddressElement.textContent = data.ip_address;
    networkElement.textContent = data.network;
  });

// Get available network adapters and update the select element
setInterval(() => {
  fetch('/adapters')
    .then((response) => response.json())
        .then((adapters) => {
      // Clear the select element
      adapterSelect.innerHTML = '';
      // Add the available adapters as options
      adapters.forEach((adapter) => {
        const option = document.createElement('option');
        option.value = adapter;
        option.textContent = adapter;
        adapterSelect.appendChild(option);
      });
    });
}, 3000);

// Update the terminal output every second
setInterval(() => {
  fetch('/terminal-output')
    .then((response) => response.text())
    .then((output) => {
      terminalOutput.textContent = output;
      // Scroll to the bottom of the terminal output
      terminalOutput.scrollTop = terminalOutput.scrollHeight;
    });
}, 1000);

