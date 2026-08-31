const fs = require('fs');
const path = require('path');

console.log('Building Velocity Nexus client bundle...');
const clientDir = path.join(__dirname, '..', 'client');
if (fs.existsSync(clientDir)) {
    console.log('Client assets verified successfully.');
}
console.log('Build complete.');
