<template>
    <h1>Virtual Triage</h1>
    <p>Enter symptoms and severity below.</p>
    <div class="symptoms-and-severity">
        <div class="symptom-input">
            <label for="symptom">Symptom:</label>
            <input type="text" id="symptom" name="symptom" required maxlength="20"/>
        </div>
        <div class="dropdown">
            <label for="severity">Severity:</label>
            <button type="button" onclick="severity()" class="dropbtn">Dropdown</button>
            <div id="severity" class="dropdown-content">
                <a>High</a>
                <a>Medium</a>
                <a>Low</a>
            </div>
        </div>
    </div>
    <div>
        <button>Submit</button>
    </div>
</template>

<script>
export default {
  name: 'VirtualTriagePage',
  props: {
    msg: String
  }
}
</script>