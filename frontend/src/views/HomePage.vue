<template>
  <div class="homepage-container">
    <div class="homepage-content">
      <h1>Добро пожаловать!</h1>
      <p>Это главная страница.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.homepage-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #232046 0%, #2d223a 100%);
}
.homepage-content {
  background: rgba(30, 27, 52, 0.85);
  border-radius: 18px;
  padding: 48px 32px;
  box-shadow: 0 4px 32px 0 rgba(80, 60, 180, 0.12);
  text-align: center;
}
h1 {
  color: #c7bfff;
  font-size: 2.2rem;
  margin-bottom: 18px;
  font-weight: 700;
}
p {
  color: #b3b3c6;
  font-size: 1.1rem;
}
</style>
