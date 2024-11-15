<template>
  <div class="manage-appointment">
    <NavbarAppointment />
    <div class="container-fluid mt-5 pt-3">
      <div class="row">
        <!-- Left Section: Triage Result -->
        <div class="col-4 border-end">
          <h3 class="text-center mb-3 fw-bold mt-1">Triage Results</h3>
          <ul class="list-group">
            <li class="list-group-item" v-for="(patient, index) in triageResults" :key="index">
              {{ patient.name }} - {{ patient.severity }} Priority
            </li>
          </ul>
        </div>
        <!-- Right Section: Schedule with Dynamic Hours and Drag-and-Drop -->
        <div class="col-8">
          <h3 class="text-center mb-3 fw-bold mt-1">Schedule</h3>
          <div class="schedule">
            <div v-for="hour in hours" :key="hour" class="time-slot d-flex align-items-center border-bottom"
              @dragover.prevent="dragOver" @drop="drop($event, hour)">
              <div class="time-label">{{ hour }}:00 - {{ (hour + 1) % 24 }}:00</div>
              <div
                v-for="(patient, index) in appointments[hour] || []"
                :key="index"
                class="list-group-item schedule-item"
                :class="{
                  'high-severity': patient.severity === 'High',
                  'medium-severity': patient.severity === 'Medium',
                  'low-severity': patient.severity === 'Low'
                }"
                :title="patient.name"
                draggable="true"
                @dragstart="dragStart($event, patient)"
                @click="openPatientModal(patient)"
              >
                {{ patient.name }}
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
                      <p><strong>Name:</strong> {{ selectedPatient.name }}</p>
                      <p><strong>Address:</strong> {{ selectedPatient.address }}</p>
                      <p><strong>Phone Number:</strong> {{ selectedPatient.phone_number }}</p>
                      <p><strong>Insurance:</strong> {{ selectedPatient.insurance }}</p>
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { Modal } from 'bootstrap';
import NavbarAppointment from './NavbarAppointment.vue';
// import axios from 'axios';

export default {
  name: 'ManageAppointment',
  components: {
    NavbarAppointment,
  },
  setup() {
    // Mock data for triage results and appointments
    const triageResults = ref([
      { name: 'John Doe', severity: 'High', address: '123 Street', phone_number: '123-456-7890', insurance: 'XYZ123', description: 'Severe pain', created_at: '2023-01-01 10:00' },
      { name: 'Jane Smith', severity: 'Medium', address: '456 Avenue', phone_number: '987-654-3210', insurance: 'ABC456', description: 'Moderate injury', created_at: '2023-01-01 11:00' },
      { name: 'Alice Brown', severity: 'Low', address: '789 Boulevard', phone_number: '555-123-4567', insurance: 'DEF789', description: 'Minor injury', created_at: '2023-01-01 12:00' },
    ]);

    const hours = ref(Array.from({ length: 24 }, (_, i) => i)); // Current day hours
    const appointments = ref({
      10: [triageResults.value[0]],
      11: [triageResults.value[1]],
      12: [triageResults.value[2]],
    });
    const selectedPatient = ref({});

    // Drag-and-drop state
    const draggedItem = ref(null);

    const openPatientModal = (patient) => {
      selectedPatient.value = patient;
      const modal = new Modal(document.getElementById('patientInfoModal'));
      modal.show();
    };

    return {
      triageResults,
      hours,
      appointments,
      draggedItem,
      selectedPatient,
      openPatientModal
    };
  },
  methods: {
    dragStart(event, patient) {
      this.draggedItem = patient;
      event.dataTransfer.setData('text/plain', patient.id);
      event.dataTransfer.effectAllowed = 'move';
    },

    dragOver(event) {
      event.preventDefault();
    },

    drop(event, hour) {
      event.preventDefault();
      const patient = this.draggedItem;
      if (patient) {
        // Remove patient from original slot
        const originalSlot = this.appointments[patient.list];
        if (originalSlot) {
          const index = originalSlot.indexOf(patient);
          if (index !== -1) originalSlot.splice(index, 1);
        }

        // Add to new slot
        if (!this.appointments[hour]) {
          this.appointments[hour] = [];
        }
        patient.list = hour;
        this.appointments[hour].push(patient);
        this.draggedItem = null;
      }
    },
  },
};
</script>

<style scoped>
/* Styles for the page layout */
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

.schedule-item {
  width: 150px;
  text-align: center;
  padding: 5px 10px;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: move;
  margin: 5px;
}

.high-severity { background-color: #f8d7da; color: #721c24; }
.medium-severity { background-color: #fff3cd; color: #856404; }
.low-severity { background-color: #d4edda; color: #155724; }

/* Modal Custom Styling */
.modal-content {
  border-radius: 8px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
}
</style>
