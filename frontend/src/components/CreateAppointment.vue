<template>
  <div class="create-appointment">
    <NavbarAppointment /> <!-- Imported Navbar component -->

    <!-- Create Appointment Title -->
    <h2 class="title text-center">Create Appointment</h2>

    <!-- Form Container -->
    <div class="container d-flex justify-content-center align-items-center">
      <div class="form-box mb-3 p-4"> <!-- Centered and padded form box -->
        <form @submit.prevent="submitAppointment">
          <!-- Personal Information -->
          <div class="row mb-1">
            <div class="col-md-6">
              <label for="firstName" class="form-label">First Name</label>
              <input type="text" id="firstName" v-model="firstName" class="form-control" required placeholder="Enter your first name" />
            </div>
            <div class="col-md-6">
              <label for="lastName" class="form-label">Last Name</label>
              <input type="text" id="lastName" v-model="lastName" class="form-control" required placeholder="Enter your last name" />
            </div>
          </div>

          <!-- Address -->
          <div class="mb-1">
            <label for="address" class="form-label mb-1">Address</label>
            <input type="text" id="address" v-model="address" class="form-control" required placeholder="Enter your address" />
          </div>

          <!-- Phone Number -->
          <div class="mb-1">
            <label for="phone" class="form-label mb-1">Phone Number</label>
            <input
              type="tel"
              id="phone"
              v-model="phoneNumber"
              class="form-control"
              required
              placeholder="Enter your phone number"
              pattern="^(\+?\d{1,3}[- ]?)?\d{10}$"
            />
            <small class="form-text text-muted">We will text you when your turn in the ER is ready.</small>
          </div>

          <!-- Health Insurance Number -->
          <div class="mb-1">
            <label for="insurance" class="form-label mb-1">Health Insurance Number</label>
            <input type="text" id="insurance" v-model="insuranceNumber" class="form-control" required placeholder="Enter your health insurance number" />
          </div>

          <!-- Severity Dropdown -->
          <div class="mb-1">
            <label for="severity" class="form-label mb-2">Emergency Severity</label>
            <select id="severity" v-model="severity" class="form-select" required>
              <option value="" disabled>Select severity level...</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <!-- Optional Description -->
          <div class="mb-1">
            <label for="description" class="form-label mb-1">Description of Health Emergency <small>(Optional)</small></label>
            <textarea id="description" v-model="description" class="form-control" rows="4" placeholder="Briefly describe your health concern"></textarea>
          </div>

          <!-- Book Appointment Button -->
          <button type="submit" class="btn btn-primary w-100">Book Appointment</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarAppointment from './NavbarAppointment.vue';
import Swal from 'sweetalert2';
import axios from 'axios'; // Ensure axios is imported

export default {
  components: {
    NavbarAppointment,
  },
  data() {
    return {
      firstName: '',
      lastName: '',
      address: '',
      phoneNumber: '',
      insuranceNumber: '',
      severity: '', // Bind this to the severity dropdown
      description: '',
    };
  },
  methods: {
    async submitAppointment() {
      try {
        // Send a POST request to the backend with appointment details
        await axios.post('http://localhost:5000/api/appointments', {
          first_name: this.firstName,
          last_name: this.lastName,
          address: this.address,
          phone_number: this.phoneNumber,
          insurance_number: this.insuranceNumber,
          description: this.description,
          severity: this.severity, // Pass severity level from the store
        });

        // Display success message
        Swal.fire({
          title: `Appointment Booked!`,
          text: `You have successfully put ${this.firstName} ${this.lastName} on the queue. They will receive a text with their scheduled appointment time.`,
          icon: 'success',
          confirmButtonText: 'OK',
          background: '#d9f7ff', // Light blue background color
          color: '#333', // Dark text color for contrast
          confirmButtonColor: '#4CAF50', // Green color for confirm button
          iconColor: '#4CAF50', // Icon color to match the theme
          customClass: {
            popup: 'custom-swal-popup',
            title: 'custom-swal-title',
            content: 'custom-swal-content',
          },
        });

        this.resetForm(); // Clear the form fields after successful submission
      } catch (error) {
        console.error('Error booking appointment:', error);

        // Display error message
        Swal.fire({
          title: 'Error',
          text: 'An error occurred while booking the appointment. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK',
        });
      }
    },
    resetForm() {
      this.firstName = '';
      this.lastName = '';
      this.address = '';
      this.phoneNumber = '';
      this.insuranceNumber = '';
      this.severity = '';
      this.description = '';
    },
  },
};
</script>


<style scoped>
/* Title Styling */
.title {
  font-size: 2rem;
  color: #333;
  margin-top: 80px;
  text-align: center;
}

/* Center and constrain form box */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.form-box {
  max-width: 600px;
  width: 100%;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Styling for the alert message */
.custom-swal-popup {
  border-radius: 8px;
  padding: 20px;
}

.custom-swal-title {
  font-size: 1.5rem;
  color: #4CAF50;
}

.custom-swal-content {
  font-size: 1rem;
}
</style>
