<template>
  <div id="app">
    <div class="loginBox">
      <div class="inner">
        <div class="register">
          <div class="top">
            <img class="logo" src="https://www.mistered.de/MisterEDk.png" />
            <div class="title">Create an Account</div>
            <div class="subtitle">
              Already have an account?
              <router-link class="subtitle-action" to="/">Sign In</router-link>
            </div>
          </div>

          <form @submit.prevent="signUp">
            <div class="form">
              <input
                type="text"
                placeholder="First Name"
                v-model="firstName"
                class="w100"
                required
              />
              <input
                type="text"
                placeholder="Last Name"
                v-model="lastName"
                class="w100"
                required
              />
              <input
                type="text"
                placeholder="Employee ID"
                v-model="employeeId"
                class="w100"
                required
              />
              <input
                type="password"
                placeholder="Password"
                v-model="password"
                class="w100"
                required
              />
              <input
                type="password"
                placeholder="Confirm Password"
                v-model="confirmPassword"
                class="w100"
                required
              />
            </div>

            <button type="submit" class="action" :disabled="!registerValid">
              Create Account
            </button>
          </form>

          <!-- Error and Success Messages -->
          <p v-if="error" class="error-message">{{ error }}</p>
          <p v-if="success" class="success-message">{{ success }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      employeeId: '',
      password: '',
      confirmPassword: '',
      error: '',
      success: ''
    };
  },
  computed: {
    registerValid() {
      return (
        this.firstName &&
        this.lastName &&
        this.employeeId &&
        this.password &&
        this.confirmPassword &&
        this.password === this.confirmPassword
      );
    }
  },
  methods: {
    signUp() {
      // Check if passwords match
      if (this.password !== this.confirmPassword) {
        this.error = "Passwords do not match!";
        setTimeout(() => (this.error = ''), 3000);
        return;
      }

      // Simulate successful registration
      this.success = "Registration successful! Please log in.";
      this.error = ""; // Clear any existing error message
      this.clearForm();

      // Redirect to sign-in page after a delay
      setTimeout(() => {
        this.$router.push('/');
      }, 2000);
    },
    clearForm() {
      this.firstName = '';
      this.lastName = '';
      this.employeeId = '';
      this.password = '';
      this.confirmPassword = '';
      this.error = '';
      this.success = '';
    }
  }
};
</script>

<style lang="scss" scoped>
html, body, #app {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  margin-bottom: 20px;
}

@mixin box {
  box-shadow: 1px 1px 2px 1px #ccc;
}

@mixin field {
  border: 1px solid #aaa;
  height: 40px;
  padding: 10px;
  margin-top: 20px;
  border-radius: 5px;
  box-sizing: border-box;
}

input[type="text"],
input[type="password"] {
  @include field;
}

.invalid {
  border: 2px solid red !important;
  &::placeholder {
    color: red;
  }
}

.w100 {
  width: 100%;
}

.logo {
  width: 290px;
  margin-bottom: 0;
}

.action {
  height: 40px;
  text-transform: uppercase;
  border-radius: 25px;
  width: 100%;
  border: none;
  cursor: pointer;
  background: rgb(18, 171, 99);
  margin-top: 20px;
  color: #fff;
  font-size: 1.2rem;
  @include box;
}

.action:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.top {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-bottom: 0;
  padding-top: 10px;
}

.title {
  width: 100%;
  font-size: 1.8rem;
  margin: 0;
  text-align: center;
  padding-top: 10px;
}

.subtitle {
  .subtitle-action {
    color: rgb(23, 141, 94);
    font-weight: bold;
    cursor: pointer;
  }
}

html {
  background-repeat: no-repeat;
  background: linear-gradient(
    to bottom,
    rgba(96, 108, 136, 1) 0%,
    rgba(63, 76, 107, 1) 100%
  );
  background-size: cover;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-family: sans-serif;
}

.loginBox {
  background: #fff;
  border-radius: 15px;
  max-width: 400px;
  padding: 25px 55px;
  margin-top: 50px;
  animation: slideInTop 1s;
}

@keyframes slideInTop {
  from {
    opacity: 0;
    transform: translateY(-30%);
  }
  to {
    opacity: 100;
    transform: translateY(0%);
  }
}

@media screen and (min-width: 440px) {
  .loginBox {
    @include box;
  }
}

@media screen and (max-width: 440px) {
  html {
    background: #fff;
    align-items: start;
    justify-content: start;
  }
  .loginBox {
    padding: 25px 25px;
    max-width: 100vw;
    max-height: 600px;
  }
}
</style>
