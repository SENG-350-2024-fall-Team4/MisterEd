<template>
  <nav class="navbar bg-body-tertiary fixed-top backgroung-info">
    <div class="container-fluid">
      <!-- Page title as a clickable route -->
      <router-link :to="pageRoute" class="navbar-brand fw-bold">{{ pageTitle }}</router-link>

      <h5 class="offcanvas-title ms-auto me-3 fw-bold" id="offcanvasNavbarLabel">{{ username }}</h5>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="offcanvas"
        data-bs-target="#offcanvasNavbar"
        aria-controls="offcanvasNavbar"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title fw-bold" id="offcanvasNavbarLabel">{{ username }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
            <li class="nav-item">
              <router-link class="nav-link active" to="/home-page" @click="closeOffcanvas">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/create-appointment" @click="closeOffcanvas">Create Appointment</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/manage-appointment" @click="closeOffcanvas">Manage Appointments</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link active" to="/" @click.prevent="logout">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import * as bootstrap from 'bootstrap';

export default {
  name: 'NavbarAppointment',
  setup() {
    const route = useRoute();
    const router = useRouter();

    const username = ref("Username"); // Placeholder value; replace with actual user data if available

    const pageTitle = computed(() => {
      switch (route.name) {
        case 'CreateAppointment':
          return 'Create Appointment';
        case 'ManageAppointment':
          return 'Manage Appointments';
        case 'EditProfile':
          return 'Edit Profile';
        case 'HomePage':
          return 'Home';
        default:
          return 'Manage Appointments';
      }
    });

    const pageRoute = computed(() => {
      switch (pageTitle.value) {
        case 'Home':
          return '/home-page';
        case 'Create Appointment':
          return '/create-appointment';
        case 'Manage Appointments':
          return '/manage-appointment';
        case 'Edit Profile':
          return '/edit-profile';
        default:
          return '/home-page';
      }
    });

    // Function to close the offcanvas manually
    const closeOffcanvas = () => {
      const offcanvasElement = document.getElementById('offcanvasNavbar');
      if (offcanvasElement) {
        const offcanvasInstance = bootstrap.Offcanvas.getOrCreateInstance(offcanvasElement);
        offcanvasInstance.hide();
      }
    };

    // Logout function that redirects to the main page
    const logout = () => {
      // Add logout logic here, such as clearing session data if needed
      router.push('/');
    };

    return {
      pageTitle,
      pageRoute,
      username,
      closeOffcanvas,
      logout,
    };
  },
};
</script>

<style scoped>
/* Style adjustments for the navbar */
.navbar-brand {
  font-weight: bold;
}

.offcanvas-title {
  font-weight: bold;
}

/* Make the navbar pop up with shadow and a bottom border */
.navbar {
  background-color: #f8f9fa; /* Light background color to distinguish the navbar */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow effect for elevation */
  border-bottom: 2px solid #dee2e6; /* Border to clearly define the end of the navbar */
}

.navbar-brand {
  font-weight: bold;
}

.offcanvas-title {
  font-weight: bold;
}

</style>