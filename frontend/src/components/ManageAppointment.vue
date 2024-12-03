<template>
  <div class="manage-appointment">
    <NavbarAppointment />
    <div class="container-fluid mt-5 pt-3">
      <div class="row">
        <!-- Left Section: Triage Result -->
        <div class="col-4 border-end">
          <h3 class="text-center mb-3 fw-bold mt-1">Triage Results</h3>
          <ul class="list-group">
            <li
              class="list-group-item"
              v-for="(patient, index) in triageResults"
              :key="index"
              draggable="true"
              @dragstart="dragStart($event, patient)"
            >
              {{ patient.first_name }} {{ patient.last_name }} - {{ patient.severity || 'Unknown' }} Priority
            </li>
          </ul>
        </div>

        <!-- Right Section: Schedule -->
        <div class="col-8">
          <h3 class="text-center mb-3 fw-bold mt-1">Schedule</h3>
          <div class="schedule">
            <div
              v-for="hour in hours"
              :key="hour"
              class="time-slot d-flex align-items-center border-bottom"
              @dragover.prevent="dragOver"
              @drop="drop($event, hour)"
            >
              <div class="time-label">{{ hour }}:00 - {{ (hour + 1) % 24 }}:00</div>
              <div
                  v-for="(patient, index) in appointments[hour] || []"
                  :key="index"
                  class="list-group-item schedule-item"
                  :class="{
                    'high-severity': patient.severity === 'High',
                    'medium-severity': patient.severity === 'Medium',
                    'low-severity': patient.severity === 'Low',
                  }"
                  draggable="true"
                  @dragstart="dragStart($event, patient)"
                  @click="openPatientModal(patient)"
              >
                  <span
                    :style="{
                      color: patient.severity === 'High' ? '#721c24' :
                            patient.severity === 'Medium' ? '#856404' : '#155724'
                    }"
                  >
                    {{ patient.first_name }} {{ patient.last_name }}
                  </span>
                </div>

            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Patient Info Modal -->
    <div
      class="modal fade"
      id="patientInfoModal"
      tabindex="-1"
      aria-labelledby="patientInfoModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="patientInfoModalLabel">Patient Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p><strong>Name:</strong> {{ selectedPatient.first_name }} {{ selectedPatient.last_name }}</p>
            <p><strong>Address:</strong> {{ selectedPatient.address }}</p>
            <p><strong>Phone Number:</strong> {{ selectedPatient.phone_number }}</p>
            <p><strong>Insurance:</strong> {{ selectedPatient.insurance_number }}</p>
            <p><strong>Description:</strong> {{ selectedPatient.description }}</p>
            <p><strong>Booking Time:</strong> {{ selectedPatient.created_at }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Modal } from 'bootstrap';
import NavbarAppointment from './NavbarAppointment.vue';

export default {
  name: 'ManageAppointment',
  components: {
    NavbarAppointment,
  },
  setup() {
    const triageResults = ref([]);
    const hours = ref(Array.from({ length: 24 }, (_, i) => i)); // Hours 0 to 23
    const appointments = ref({}); // Appointments grouped by hour
    const selectedPatient = ref({});
    const draggedItem = ref(null);

    // Fetch triage results and schedule from API
    const fetchTriageResults = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/appointments/triage-results');
        const data = await response.json();
        triageResults.value = data.triage_results || [];
        appointments.value = data.schedule || {};
      } catch (error) {
        console.error('Error fetching triage results:', error);
      }
    };

    // Open patient details modal
    const openPatientModal = (patient) => {
      selectedPatient.value = patient;
      const modal = new Modal(document.getElementById('patientInfoModal'));
      modal.show();
    };

    // Lifecycle hook to fetch data on mount
    onMounted(fetchTriageResults);

    return {
      triageResults,
      hours,
      appointments,
      draggedItem,
      selectedPatient,
      openPatientModal,
    };
  },
  methods: {
    dragStart(event, patient) {
      this.draggedItem = patient;
      event.dataTransfer.effectAllowed = 'move';
    },
    dragOver(event) {
      event.preventDefault();
    },
    async drop(event, hour) {
      event.preventDefault();
      const patient = this.draggedItem;

      if (patient) {
        // Remove patient from triage results
        const index = this.triageResults.findIndex((p) => p.id === patient.id);
        if (index !== -1) {
          this.triageResults.splice(index, 1);
        }

        // Add patient to schedule
        if (!this.appointments[hour]) {
          this.appointments[hour] = [];
        }
        this.appointments[hour].push(patient);

        this.draggedItem = null;

        // Update the backend with the new schedule
        try {
          await fetch('http://localhost:5000/api/appointments/update-schedule', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              id: patient.id,
              schedule_time: hour,
            }),
          });
        } catch (error) {
          console.error('Error updating schedule:', error);
        }
      }
    },
  },
};
</script>



<style scoped>
.manage-appointment {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.container-fluid {
  flex: 1;
}
.row {
  height: 88vh; /* Set a fixed height for the content area */
}
/* Left Section: Triage Results */
.col-4 {
  overflow-y: auto;
  max-height: 100%;
}

/* Right Section: Schedule */
.col-8 {
  overflow-y: auto;
  max-height: 100%;
}
/* Sticky Title */
h3 {
  position: sticky;
  top: 0;
  background-color: #ffffff;
  z-index: 1;
  padding: 10px 0;
}

/* Schedule */
.schedule {
  margin-top: 20px;
}

.time-slot {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f9f9f9;
}

.time-label {
  width: 100px;
  font-weight: bold;
  flex-shrink: 0;
}

.list-group-item {
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
}


/* Modal Custom Styling */
.modal-content {
  border-radius: 8px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
}
/* Update styles */
.list-group-item {
  padding: 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
}

/* .schedule-item {
  padding: 10px 15px;
  font-size: 14px;
} */
.schedule-item {
  width: 150px;
  text-align: center;
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
} 

.high-severity { 
  background-color: #f8d7da; 
  border: 1px solid #f5c6cb;
}

.medium-severity { 
  background-color: #fff3cd;
  border: 1px solid #ffeeba; 
  
}

.low-severity { 
  background-color: #89ba95;
  border: 1px solid #c3e6cb;
  
}

</style>
