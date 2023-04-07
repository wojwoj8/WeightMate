const fats = document.querySelector('#fats');
const proteins = document.querySelector('#proteins');
const carbohydrates = document.querySelector('#carbohydrates');
const totalCaloriesH2 = document.querySelector('.total_calories');
const inputKcal = document.querySelector('#kcal');

function calculateTotalCalories() {
  let kcal = 0;
  if (fats.value === '' || proteins.value === '' || carbohydrates.value === '') {
    kcal = 0;
  } else {
    const fatsValKcal = fats.value * 9;
    const protValKcal = proteins.value * 4;
    const carbValKcal = carbohydrates.value * 4;
    kcal = fatsValKcal + protValKcal + carbValKcal;
  }

  // console.log(kcal);
  totalCaloriesH2.textContent = `Total calories ${kcal}`;
  inputKcal.value = kcal;
}

fats.addEventListener('input', calculateTotalCalories);
proteins.addEventListener('input', calculateTotalCalories);
carbohydrates.addEventListener('input', calculateTotalCalories);
