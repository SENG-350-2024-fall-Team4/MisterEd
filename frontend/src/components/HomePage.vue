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
            <!-- Create Appointment Button -->
            <router-link to="/create-appointment" class="btn btn-primary mt-4">Create Appointment</router-link>
          </div>

          <!-- Recent Activity -->
          <div class="recent-activity card mt-4 p-4 shadow-sm">
            <h3 class="text-secondary mb-3">Recent Activity</h3>
            <ul class="list-unstyled">
              <li v-for="activity in recentActivity" :key="activity.id" class="activity-item py-2 border-bottom">
                {{ activity.message }}
              </li>
            </ul>
          </div>
          
        </div>

        <!-- Right Column: Current Schedule -->
        <div class="col-md-6">
          <div class="schedule card p-4 shadow-sm">
            <h3 class="text-success mb-3">Patients in the ER</h3>
            <div v-for="appointment in currentSchedule" :key="appointment.id" class="appointment-item py-3 border-bottom">
              <p><strong>{{ appointment.time }}</strong> - {{ appointment.patientName }} <span class="badge bg-warning text-dark">{{ appointment.priority }}</span></p>
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
      todayAppointmentsCount: 5, // Placeholder count for today's appointments
      pendingTriageCount: 2, // Placeholder count for pending triage
      recentActivity: [
        { id: 1, message: 'John Doe checked in for triage.' },
        { id: 2, message: 'Jane Smith’s appointment has been rescheduled.' },
        { id: 3, message: 'Peter Parker completed his ER visit.' }
      ], // Placeholder recent activity
      currentSchedule: [
        { id: 1, time: '10:00 AM', patientName: 'John Doe', priority: 'High' },
        { id: 2, time: '10:30 AM', patientName: 'Jane Smith', priority: 'Medium' },
        { id: 3, time: '11:00 AM', patientName: 'Peter Parker', priority: 'Low' }
      ] // Placeholder schedule
    };
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

.overview, .recent-activity, .schedule {
  padding: 20px;
}

.appointment-item, .activity-item {
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
