<template>
  <div class="home-page">
    <NavbarAppointment />

    <div class="container mt-5">
      <div class="row">
        <!-- Left Column: Overview and Recent Activity -->
        <div class="col-md-6">
          <!-- Today's Overview -->
          <div class="overview card mb-3 p-4 shadow-sm">
            <h3 class="text-info mb-3">Today's Overview</h3>
            <ul class="list-unstyled">
              <li><strong>Appointments:</strong> {{ todayAppointmentsCount }}</li>
              <li><strong>Pending Triage:</strong> {{ pendingTriageCount }}</li>
            </ul>
            <router-link to="/create-appointment" class="btn btn-primary mt-4">Create Appointment</router-link>
          </div>

          <!-- Recent Activity -->
          <div class="recent-activity card mt-4 p-4 shadow-sm">
            <h3 class="text-secondary mb-3">Recent Activity</h3>
            <ul class="list-unstyled">
              <li
                v-for="activity in recentActivity"
                :key="activity.id"
                class="activity-item py-2 border-bottom"
              >
                {{ activity.message }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Right Column: Current Schedule -->
        <div class="col-md-6">
          <div class="schedule card p-4 shadow-sm">
            <h3 class="text-success mb-3">Patients in the ER</h3>
            <div
              v-for="appointment in currentSchedule"
              :key="appointment.id"
              class="appointment-item py-3 border-bottom"
            >
              <p>
                <strong>{{ appointment.time }}</strong> - {{ appointment.patientName }}
                <span class="badge bg-warning text-dark">{{ appointment.priority }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarAppointment from './NavbarAppointment.vue';

export default {
  name: 'HomePage',
  components: {
    NavbarAppointment,
  },
  data() {
    return {
      todayAppointmentsCount: 0,
      pendingTriageCount: 0,
      recentActivity: [],
      currentSchedule: [], // Stores patients in the ER
    };
  },
  methods: {
    async fetchTodayOverview() {
      try {
        const response = await fetch('http://localhost:5000/api/appointments/today-overview');
        const data = await response.json();
        console.log("here is the data: ", data);
        this.todayAppointmentsCount = data.appointments;
        this.pendingTriageCount = data.pending_triage;
      } catch (error) {
        console.error('Error fetching Today\'s Overview:', error);
      }
    },
    async fetchRecentActivity() {
      try {
        const response = await fetch('http://localhost:5000/api/appointments/recent-activity');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        this.recentActivity = data.recent_activity.map(activity => ({
          id: activity.id,
          message: activity.message,
        }));
      } catch (error) {
        console.error('Error fetching Recent Activity:', error);
      }
    },
    async fetchCurrentSchedule() {
      try {
        const response = await fetch('http://localhost:5000/api/appointments/current-schedule', {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        this.currentSchedule = data.scheduled_patients.map(patient => ({
          id: patient.id,
          time: patient.time,
          patientName: patient.patientName,
          priority: patient.priority,
        }));
      } catch (error) {
        console.error('Error fetching Current Schedule:', error);
      }
    },
  },
  mounted() {
    this.fetchTodayOverview();
    this.fetchRecentActivity();
    this.fetchCurrentSchedule();
  },
};
</script>


<style scoped>
.home-page {
  background-color: #f5f7fa;
  padding: 30px 20px;
  font-family: Arial, sans-serif;
}

.card {
  background-color: #ffffff;
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h3 {
  font-weight: bold;
}

.text-primary {
  color: #06080e;
}

.overview,
.recent-activity,
.schedule {
  padding: 20px;
}

.appointment-item,
.activity-item {
  font-size: 0.9em;
}

.appointment-item p {
  margin: 0;
}

.badge {
  font-size: 0.75em;
  padding: 5px 10px;
  border-radius: 10px;
}

.btn-primary {
  background-color: #0ed482;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #256d4b;
}

.container {
  max-width: 900px;
}
</style>
