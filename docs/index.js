import { parseSwitch, solveLock } from './switches.js'


const NUM_SWITCHES = 8;

const switches = [];

const spinnerEl = document.getElementById('spinner');





for (let i = 0; i < NUM_SWITCHES; ++i) {
  const switchEl = document.getElementById(`switch-${i}`);
  switches.push(switchEl);
}


function onSolve(ev) {
  ev.preventDefault();


  
  
  
  try {    
    const inpuVoltageEl = document.getElementById('input-voltage-ui');
    const outputVoltageRedEl = document.getElementById('expected-voltage-red-ui');
    const outputVoltageBlueEl = document.getElementById('expected-voltage-blue-ui');
    
    const switchesEls = [];
    for (let i = 0; i < NUM_SWITCHES * 2; ++i) {
      const switchEl = document.getElementById(`switch-input-${i}`);
      switchesEls.push(switchEl);
    }
  
    const initialVoltages = [inpuVoltageEl.value, inpuVoltageEl.value].map(Number);
    const expectedVoltages = [outputVoltageRedEl.value, outputVoltageBlueEl.value].map(Number);
    
    // Zip in pairs
    let switches = switchesEls.reduce(function(result, value, index, array) {
      if (index % 2 === 0)
        result.push(array.slice(index, index + 2));
      return result;
    }, []);
  
    switches = switches.map(r => r.map(s => parseSwitch(s.value)))
    updateElementInnerHtml('input-voltage', initialVoltages[0]);
    updateElementInnerHtml('output-voltage-red', expectedVoltages[0]);
    updateElementInnerHtml('output-voltage-blue', expectedVoltages[1]);

    const solution = solveLock(initialVoltages, expectedVoltages, switches);
    if (!solution) {
      alert('No se encontró solución');
      switches.forEach((switchEl, i) => updateSwitch(i, false));
      return;
    }

    solution.forEach((checked, i) => updateSwitch(i, checked));

  } catch (err) {
    alert(err.message);
    return;
  }


}

function updateSwitch(index, checked) {
  const switchEl = switches[index];
  switchEl.checked = checked;
}

function updateElementInnerHtml(id, innerHtml) {
  const el = document.getElementById(id);
  el.innerHTML = innerHtml;
}

function toggleSpinner() {
  spinnerEl.classList.toggle('d-none');
}

const solveBtn = document.getElementById('solve-btn');
solveBtn.addEventListener('click', onSolve);

const imageInput = document.getElementById('input-image');
imageInput.addEventListener('input', (ev) => {
  const file = ev.target.files[0];

  const data = new FormData();
  data.append('image', file);

  toggleSpinner();
  fetch('http://192.168.1.124:5000/image-params',
    {
      method: 'POST',
      body: data
    })
    .then(res => res.json())
    .then(({ input_voltage, expected_voltages, switches, input_voltage_image, expected_voltages_images, switches_images }) => {

 

      setImage(input_voltage_image, 'input-voltage-img');
      setElValue('input-voltage-ui', input_voltage);

      setImage(expected_voltages_images[0], 'expected-voltage-red-img');
      setElValue('expected-voltage-red-ui', expected_voltages[0]);
      setImage(expected_voltages_images[1], 'expected-voltage-blue-img');
      setElValue('expected-voltage-blue-ui', expected_voltages[1]);

      const switchesUiEl = document.getElementById('switches-ui');
      const switchesimg = switches_images.flat()
      const switchesdata = switches.flat();
      switchesimg.forEach((b64Image, i) => {
        
        setImage(b64Image, `switch-input-${i}-img`);
        setElValue(`switch-input-${i}`, switchesdata[i]);
      })
    })
    .catch(err => {
      console.error(err);
      alert('No se pudo procesar la imagen');
    })
    .finally(() => {
      toggleSpinner();
    })
})


function setImage(b64Image, id) {
  const file = imageInput.files[0];

  const prefix = `data:image/${file.name.split('.').pop()};base64,`;
  b64Image = prefix + b64Image;
  const el = document.getElementById(id);
  el.src = b64Image;
}

function setElValue(id, value) {
  const el = document.getElementById(id);
  el.value = value;
}
