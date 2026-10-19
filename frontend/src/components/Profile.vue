<script setup>
import { ref } from "vue"

const emit = defineEmits(["signout", "delete"])

const menuOpen = ref(false)

function signOut() {
  menuOpen.value = false
  emit("signout")
}

function deleteAccount() {
  menuOpen.value = false
  emit("delete")
}
</script>

<template>
  <div class="profile">
    <button
      class="picture"
      @click="menuOpen = !menuOpen"
      aria-label="Toggle profile menu"
      :aria-expanded="menuOpen"
    >
      👤
    </button>

    <div v-if="menuOpen" class="account">
      <button @click="signOut">Sign Out</button>
      <button @click="menuOpen = false">Edit Profile</button>
      <button @click="deleteAccount">Delete Account</button>
    </div>
  </div>
</template>


<style scoped>
.profile {
  position: fixed;
  top: 16px;
  right: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  z-index: 99999;
}

/* Profile icon */
.picture {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  border: 1px solid #49415f;
  border-radius: 50%;
  background: #29243a;
  color: #c4b5fd;
  font-size: 22px;
  cursor: pointer;
}

.picture:hover {
  background: #443663;
}

/* Dropdown panel */
.account {
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 155px;
  padding: 7px;
  background: #191e29;
  border: 1px solid #353b4b;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

/* Menu buttons */
.account button {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: 6px;
  background: #29243a;
  color: #e8eaf2;
  font-size: 13px;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}

.account button:hover {
  background: #443663;
  border-color: #49415f;
}

/* Delete Account */
.account button:last-child {
  color: #fca5a5;
  background: #30212b;
  border-color: #50303f;
}

.account button:last-child:hover {
  background: #482633;
  border-color: #854052;
}
</style>