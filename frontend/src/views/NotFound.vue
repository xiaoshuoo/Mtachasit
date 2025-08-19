<template>
  <div class="notfound-container">
    <div class="notfound-content">
      <h1>404</h1>
      <p>Страница не найдена</p>
      <router-link to="/" class="back-btn">На главную</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.notfound-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #232046 0%, #2d223a 100%);
}
.notfound-content {
  background: rgba(30, 27, 52, 0.85);
  border-radius: 18px;
  padding: 48px 32px;
  box-shadow: 0 4px 32px 0 rgba(80, 60, 180, 0.12);
  text-align: center;
}
h1 {
  color: #ffb3b3;
  font-size: 3.2rem;
  margin-bottom: 18px;
  font-weight: 700;
}
p {
  color: #b3b3c6;
  font-size: 1.1rem;
  margin-bottom: 24px;
}
.back-btn {
  display: inline-block;
  padding: 10px 24px;
  background: linear-gradient(90deg, #a78bfa 0%, #f472b6 100%);
  color: #fff;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s;
}
.back-btn:hover {
  background: linear-gradient(90deg, #f472b6 0%, #a78bfa 100%);
}
</style>
