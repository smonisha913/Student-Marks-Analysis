// Small UI improvements: simple validation and subtle input animations.
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  form.addEventListener('submit', function(e){
    const name = form.querySelector('input[name="name"]');
    if (!name || !name.value.trim()) {
      e.preventDefault();
      name.focus();
      name.style.boxShadow = '0 6px 20px rgba(239,68,68,0.12)';
      setTimeout(()=> name.style.boxShadow = '', 1800);
    }
  });

  // nice focus outline for inputs
  document.querySelectorAll('input[type="text"], input[type="number"]').forEach(inp=>{
    inp.addEventListener('focus', ()=> inp.classList.add('focused'));
    inp.addEventListener('blur', ()=> inp.classList.remove('focused'));
  });
});
