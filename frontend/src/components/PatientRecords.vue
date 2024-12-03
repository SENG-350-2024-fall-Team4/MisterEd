<template>
    <div class="patient-records">
      <NavbarAppointment />
      <div class="container mt-5">
        <h3 class="text-primary mb-4">Patients Records</h3>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Phone Number</th>
              <th>Address</th>
              <th>Severity</th>
              <th>Scheduled Hour</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(patient, index) in patients"
              :key="index"
              @click="goToPatientHistory(patient.first_name, patient.last_name)"
              style="cursor: pointer;"
            >
              <td>{{ patient.id }}</td>
              <td>{{ patient.first_name }}</td>
              <td>{{ patient.last_name }}</td>
              <td>{{ patient.phone_number }}</td>
              <td>{{ patient.address }}</td>
              <td>{{ patient.severity }}</td>
              <td>{{ patient.scheduled_hour }}</td>
              <td>{{ patient.date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import NavbarAppointment from './NavbarAppointment.vue';
  
  export default {
    name: 'PatientRecords',
    components: {
      NavbarAppointment,
    },
    data() {
      return {
        patients: [],
      };
    },
    methods: {
      async fetchPatients() {
        try {
          const response = await fetch('http://localhost:5000/api/appointments/all-records');
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          const data = await response.json();
          this.patients = data.patients;
        } catch (error) {
          console.error('Error fetching patient records:', error);
        }
      },
      goToPatientHistory(firstName, lastName) {
        this.$router.push({
          name: 'PatientHistory',
          query: { first_name: firstName, last_name: lastName },
        });
      },
    },
    mounted() {
      this.fetchPatients();
    },
  };
  </script>
  
  <style scoped>
  .patient-records {
    background-color: #f5f7fa;
    padding: 30px 20px;
  }
  
  h3 {
    font-weight: bold;
    color: #06080e;
  }
  
  .table {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .table th {
    background-color: #0ed482;
    color: #fff;
  }
  
  .table td {
    vertical-align: middle;
  }
  </style>
  