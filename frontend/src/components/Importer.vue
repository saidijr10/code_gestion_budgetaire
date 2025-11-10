<template>
  <div>
    <input type="file" @change="handleFileUpload" />
    <button @click="importerBudget" :disabled="!fichier">Importer</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const fichier = ref(null)
const message = ref('')

function handleFileUpload(event) {
  fichier.value = event.target.files[0]
}

async function importerBudget() {
  if (!fichier.value) return

  const formData = new FormData()
  formData.append('fichier_excel', fichier.value)

  try {
    const res = await fetch('/api/import-budget/', {
      method: 'POST',
      body: formData,
    })
    if (!res.ok) throw new Error('Erreur lors de l\'import')

    message.value = 'Import réussi !'
    // Recharge la liste de budgets si besoin
  } catch (e) {
    message.value = e.message
  }
}
</script>
