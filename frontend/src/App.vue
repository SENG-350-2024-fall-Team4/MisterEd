<template>
  <div id="app">
    <ManageAppointment />
  </div>
</template>

<script>
import ManageAppointment from './components/ManageAppointment.vue'; // Ensure the path is correct

export default {
  name: 'App',
  components: {
    ManageAppointment,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
