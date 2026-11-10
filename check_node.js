
const fs = require('fs');
const vm = require('vm');
const code = fs.readFileSync('test_app.js', 'utf8');
try {
  new vm.Script(code, { filename: 'test_app.js' });
  console.log('Valid JS!');
} catch (err) {
  console.log('Error name:', err.name);
  console.log('Error message:', err.message);
  console.log('Stack:', err.stack);
}
