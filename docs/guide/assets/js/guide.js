// A TeX command should be searchable both as `integral` and `\integral`.
// Capture runs before the theme's input handler reads the query.
document.addEventListener('input', function (event) {
  if (event.target.id === 'search-input' && event.target.value.includes('\\')) {
    event.target.value = event.target.value.replace(/\\/g, '');
  }
}, true);
