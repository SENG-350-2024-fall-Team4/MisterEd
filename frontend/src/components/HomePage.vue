<template>
  <div id="homepage">
    <div class="navbar">
      <img
        class="logo"
        src="https://www.mistered.de/MisterEDk.png"
        alt="Mister Ed Logo"
      />
      <div class="menu">
        <span class="menu-item" @click="navigateTo('triage')">Virtual Triage</span>
        <span class="menu-item" @click="navigateTo('load')">ED Load</span>
        <span class="menu-item" @click="navigateTo('profile')">Patient Info</span>
        <span class="menu-item logout" @click="logout">Logout</span>
      </div>
    </div>
    
    <div class="content">
      <h1>Welcome to Mister Ed!</h1>
      <p>Use the navigation above to explore features like Virtual Triage, current ED load, and manage your patient information.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",

  methods: {
    navigateTo(section) {
      // Handle navigation based on section
      console.log(`Navigating to ${section}`);
      // This could be expanded with a router to actually handle navigation
    },

    logout() {
      console.log("Logging out");
      // Handle the logout logic and navigate back to login
      this.$router.push({ name: 'LoginView' });
    }
  }
};
</script>

<style scoped>
#homepage {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 20px;
  text-align: center;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #2c3e50;
  color: white;
}

.logo {
  width: 150px;
}

.menu {
  display: flex;
  gap: 20px;
}

.menu-item {
  cursor: pointer;
  font-weight: bold;
}

.logout {
  color: red;
}

.content {
  margin-top: 50px;
}

h1 {
  color: #2c3e50;
}

p {
  font-size: 1.2rem;
  color: #555;
}
</style>
