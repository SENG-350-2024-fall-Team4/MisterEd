<template>
  <div class="book-appointment">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <!-- Logo Section -->
        <a class="navbar-brand" href="#">
          <img src="https://www.mistered.de/MisterEDk.png" alt="Logo" width="120" />
        </a>
  
        <!-- Right Side: Changed Mind question and Log out Button -->
        <div class="d-flex align-items-center ms-auto">
          <span class="fs-5 me-2 fw-bold">Changed your Mind?</span>
          <router-link to="/" class="btn btn-primary ms-2">Log Out</router-link>
        </div>
      </div>
    </nav>
    
    <h2 class="text-center mb-4 mt-3">Appointment Details</h2>
    
    <div class="container mb-3">
      <form @submit.prevent="submitAppointment">
        <!-- Personal Information -->
        <div class="row mb-2">
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
        <div class="mb-2">
          <label for="address" class="form-label">Address</label>
          <input type="text" id="address" v-model="address" class="form-control" required placeholder="Enter your address" />
        </div>

        <!-- Phone Number -->
        <div class="mb-2">
          <label for="phone" class="form-label">Phone Number</label>
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
        <div class="mb-2">
          <label for="insurance" class="form-label">Health Insurance Number</label>
          <input type="text" id="insurance" v-model="insuranceNumber" class="form-control" required placeholder="Enter your health insurance number" />
        </div>

        <!-- Optional Description -->
        <div class="mb-3">
          <label for="description" class="form-label">Description of Health Emergency <small>(Optional)</small></label>
          <textarea id="description" v-model="description" class="form-control" rows="4" placeholder="Briefly describe your health concern"></textarea>
        </div>

        <!-- Book Appointment Button -->
        <button type="submit" class="btn btn-primary w-100">Book Appointment</button>
      </form>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import { useSeverityStore } from '../store/severity'; // Ensure this store is correctly defined and imported

export default {
  setup() {
    // Use Pinia store to manage severity
    const severityStore = useSeverityStore();

    return {
      severity: severityStore.severity, // Reactive severity level from the store
    };
  },
  data() {
    return {
      firstName: '',
      lastName: '',
      address: '',
      phoneNumber: '',
      insuranceNumber: '',
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

        // Display success message on successful booking
        Swal.fire({
          title: 'Appointment Booked!',
          text: `${this.firstName} ${this.lastName}, you are put on the queue. You will receive a text with your scheduled appointment time about an hour before your appointment.`,
          icon: 'success',
          confirmButtonText: 'OK',
          background: '#d9f7ff',
          color: '#333',
          confirmButtonColor: '#4CAF50',
          iconColor: '#4CAF50',
          customClass: {
            popup: 'custom-swal-popup',
            title: 'custom-swal-title',
            content: 'custom-swal-content',
          },
        });

        // Redirect to home page after 2 seconds
        setTimeout(() => {
          this.$router.push('/');
        }, 2000);
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
  },
};
</script>


<style scoped>
.container {
  max-width: 600px;
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
