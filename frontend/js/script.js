// Carousel Auto-rotation
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
let currentSlide = 0;

function showSlide(index) {
  if (!slides.length) return;
  slides.forEach((s, i) => s.classList.toggle('active', i === index));
  dots.forEach((d, i) => d.classList.toggle('active', i === index));
}

if (slides.length > 0) {
  setInterval(() => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }, 4500);

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      currentSlide = i;
      showSlide(currentSlide);
    });
  });
}

// Multi-Step Form Navigation & Phone Enforcement
const step1 = document.getElementById('step-1');
const step2 = document.getElementById('step-2');
const btnNext = document.getElementById('btn-next');
const btnBack = document.getElementById('btn-back');
const progressBar = document.getElementById('progress-bar');
const stepLabel = document.getElementById('step-label');
const phoneInput = document.getElementById('phone');

if (phoneInput) {
  phoneInput.addEventListener('input', (e) => {
    e.target.value = e.target.value.replace(/\D/g, '').slice(0, 10);
  });
}

if (btnNext && step1 && step2) {
  btnNext.addEventListener('click', () => {
    const step1Inputs = step1.querySelectorAll('input, select');
    let isValid = true;

    step1Inputs.forEach((input) => {
      if (!input.checkValidity()) {
        input.reportValidity();
        isValid = false;
      }
    });

    if (isValid) {
      step1.classList.remove('active-step');
      step2.classList.add('active-step');
      if (progressBar) progressBar.style.width = '100%';
      if (stepLabel) stepLabel.textContent = 'Part 2: Educational & Career Goals';
    }
  });
}

if (btnBack && step1 && step2) {
  btnBack.addEventListener('click', () => {
    step2.classList.remove('active-step');
    step1.classList.add('active-step');
    if (progressBar) progressBar.style.width = '50%';
    if (stepLabel) stepLabel.textContent = 'Part 1: Personal & Contact Information';
  });
}

// Form Submission -> Package data and direct to report dashboard
const careerForm = document.getElementById('career-form');
if (careerForm) {
  careerForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const nameVal = document.getElementById('name')?.value.trim() || 'Candidate';
    const emailVal = document.getElementById('email')?.value.trim() || '';
    const countryCodeVal = document.getElementById('country-code')?.value || '+91';
    const rawPhone = document.getElementById('phone')?.value.trim() || '';
    const locationVal = document.getElementById('preferred-location')?.value.trim() || '';
    const courseVal = document.getElementById('degree-course')?.value || 'Undergraduate';
    const yearVal = document.getElementById('current-year')?.value || '';
    const collegeVal = document.getElementById('college')?.value.trim() || '';
    const skillsVal = document.getElementById('skills')?.value.trim() || 'Programming fundamentals';
    const careerFieldVal = document.getElementById('career-field')?.value.trim() || 'Software Development';
    const degreeModeVal = document.getElementById('degree-mode')?.value || 'Flexible';
    const counselingVal = document.getElementById('counseling-intent')?.value || 'no';
    const budgetVal = document.getElementById('budget')?.value || '';

    // Standardized payload matching backend pipeline & UI renderers
    const formData = {
      name: nameVal,
      email: emailVal,
      country_code: countryCodeVal,
      phone: `${countryCodeVal} ${rawPhone}`,
      preferred_location: locationVal,
      education: `${courseVal} (${yearVal ? 'Year ' + yearVal : 'Current'}, ${collegeVal || 'University'})`,
      skills: skillsVal,
      interests: careerFieldVal,
      goals: careerFieldVal,
      study_mode: degreeModeVal,
      counseling_interest: counselingVal,
      budget: budgetVal,
      // Retain original raw fields
      course: courseVal,
      year: yearVal,
      college: collegeVal,
      career_field: careerFieldVal,
      degree_mode: degreeModeVal,
      counseling_intent: counselingVal
    };

    const payloadString = JSON.stringify(formData);
    sessionStorage.setItem('assessment_payload', payloadString);
    localStorage.setItem('assessment_payload', payloadString);

    // Clear previous report so fresh analysis triggers
    sessionStorage.removeItem('careerReport');
    localStorage.removeItem('careerReport');

    window.location.href = 'report.html';
  });
}