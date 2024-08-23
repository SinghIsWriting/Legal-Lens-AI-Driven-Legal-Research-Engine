// static/js/scripts.js

document.getElementById('dark-mode-toggle').addEventListener('click', function() {
    document.body.classList.toggle('bg-dark');
    document.body.classList.toggle('text-light');
    document.getElementsByTagName('div').classList.toggle('bg-dark');
    document.getElementsByTagName('div').classList.toggle('text-light');
});
