function parseOperation(switchObj) {
  if (switchObj === null) {
    return function (x) { return x; };
  }

  const operator = switchObj.operator;
  const value = switchObj.value;

  if (operator === '+') {
    return function (x) { return x + value; };
  } else if (operator === '-') {
    return function (x) { return x - value; };
  } else if (operator === '*') {
    return function (x) { return x * value; };
  } else if (operator === '/') {
    return function (x) { return x / value; };
  } else {
    throw new Error('Invalid operator');
  }
}

function tryCombination(voltages, combination, switches) {
  for (let i = 0; i < switches.length; i++) {
    const switchRow = switches[i];
    if (!combination[i]) {
      continue;
    }
    for (let j = 0; j < voltages.length; j++) {
      voltages[j] = switchRow[j](voltages[j]);
    }
  }
  return voltages;
}

function product(iterables, repeat) {
  var argv = Array.prototype.slice.call(arguments), argc = argv.length;
  if (argc === 2 && !isNaN(argv[argc - 1])) {
    var copies = [];
    for (var i = 0; i < argv[argc - 1]; i++) {
      copies.push(argv[0].slice()); // Clone
    }
    argv = copies;
  }
  return argv.reduce(function tl(accumulator, value) {
    var tmp = [];
    accumulator.forEach(function (a0) {
      value.forEach(function (a1) {
        tmp.push(a0.concat(a1));
      });
    });
    return tmp;
  }, [[]]);
}


// Función para analizar una cadena y obtener un objeto de operación de switch
export function parseSwitch(switchStr) {
  if (!switchStr) {
    return null;
  }

  const matches = switchStr.match(/([-+*/])\s*(\d+)/);
  if (matches) {
    const operator = matches[1];
    const value = parseInt(matches[2], 10);
    return {
      operator,
      value,
    };
  } else {
    throw new Error('Invalid switch format: ' + switchStr);
  }
}

// Función para analizar una cadena de entrada y obtener los datos de switches, voltajes iniciales y voltajes esperados
export function parseInput(inputStr) {
  const lines = inputStr.trim().split('\n');

  const initialVoltage = lines[0].trim().split(' ').map(Number)[0];
  const initialVoltages = [initialVoltage, initialVoltage];

  const expectedVoltages = lines.slice(1, 3).map(line => Number(line.trim()));
  const switches = [];

  for (let i = 3; i < lines.length; i += 2) {
    const leftSwitch = parseSwitch(lines[i]);
    const rightSwitch = parseSwitch(lines[i + 1]);
    switches.push([leftSwitch, rightSwitch]);
  }

  return {
    initialVoltages,
    expectedVoltages,
    switches,
  };
}

function areArraysEqual(a, b) {
  if (a.length !== b.length) {
    return false;
  }

  for (let i = 0; i < a.length; ++i) {
    if (a[i] !== b[i]) {
      return false;
    }
  }

  return true;
}

// Función para resolver el problema de encontrar las combinaciones de switches
export function solveLock(initialVoltages, expectedVoltages, switches) {
  const operationSwitches = switches.map(row => row.map(parseOperation));
  
  // Obtener todas las combinaciones posibles de encendido/apagado de switches
  const combinations = product([false, true], switches.length);

  for (const combination of combinations) {
    const voltages = [...initialVoltages];
    const result_voltages = tryCombination(voltages, combination, operationSwitches);

    if (areArraysEqual(result_voltages, expectedVoltages))
      return combination;
  }

  return null;
}

// // Ejemplo de uso
// const inputStr = `
// 120
// 500
// 80
// /2
// +100
// +100
// -40

// /2

// +10
// +60

// *2
// /2
// +60
// *2

// *2
// `;
// const { initialVoltages, expectedVoltages, switches } = parseInput(inputStr);
// const result = solveLock(initialVoltages, expectedVoltages, switches);
// console.log("Switches para voltajes esperados:", result);
