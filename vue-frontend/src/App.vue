<script setup>
import {ref, onMounted} from "vue"
import {getHello} from "./api/hello"

const message = ref("");

onMounted(async () => {
    try {
        const data = await getHello();
        message.value = data.message;
    } catch (err) {
        console.error("API response error:", err);
    }
})
</script>

<template>
    <h1>{{ message }}</h1>
</template>

<style scoped></style>
