<template>
  <div class="container">

    <!-- Entête avec titre et bouton Ajouter -->
    <div class="header-actions">
      <h2 class="title">Liste des Budgets</h2>
      <button class="btn-add" @click="router.push('/ajouter-budget')">Ajouter</button>
    </div>

    <!-- 🔍 Filtres -->
    <div class="filters">
      <label>
        Année :
        <select v-model="selectedAnnee">
          <option value="">Toutes</option>
          <option v-for="a in anneesDisponibles" :key="a" :value="a">{{ a }}</option>
        </select>
      </label>

      <label>
        Type :
        <select v-model="selectedType">
          <option value="">Tous</option>
          <option v-for="type in typesDisponibles" :key="type" :value="type">{{ type }}</option>
        </select>
      </label>
      <div style="margin-bottom: 1rem;">
        <input type="file" ref="fileInput" @change="handleFileChange" accept=".xlsx, .xls" />
        <button class="btn-import" @click="importerExcel">Importer</button>
      </div>
    </div>

    <!-- 📋 Tableau -->
    <table class="liste-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Année</th>
          <th>Type</th>
          <th>Date de création</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="budget in paginatedBudgets" :key="budget.id">
          <td>{{ budget.id }}</td>
          <td>{{ budget.annee }}</td>
          <td>{{ budget.type }}</td>
          <td>{{ budget.date_creation }}</td>
          <td>
            <button class="btn-edit" @click="handleEdit(budget.id)">Modifier</button>
            <button class="btn-delete" @click="handleDelete(budget.id)">Supprimer</button>
            <button
              v-if="budget.type === 'depenses'"
              class="btn-export"
              @click="exporterExcel(budget.annee, budget.type)"
            >
              Exporter
            </button>
          </td>
        </tr>
        <tr v-if="filteredBudgets.length === 0">
          <td colspan="5" class="no-data">Aucun budget trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- 📄 Pagination -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-page">«</button>
      <button
        v-for="page in totalPages"
        :key="page"
        @click="goToPage(page)"
        :class="['btn-page', { active: currentPage === page }]"
      >
        {{ page }}
      </button>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-page">»</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getBudgets, deleteBudget } from '@/Services/BudgetServices.js'
import { useRouter } from 'vue-router'

const budgets = ref([])
const error = ref('')
const selectedAnnee = ref('')
const selectedType = ref('')
const currentPage = ref(1)
const itemsPerPage = 5
const router = useRouter()

async function loadBudgets() {
  try {
    budgets.value = await getBudgets()
  } catch (e) {
    error.value = 'Erreur lors du chargement des budgets.'
    console.error(e)
  }
}
onMounted(loadBudgets)

const anneesDisponibles = computed(() => [...new Set(budgets.value.map(b => b.annee))])
const typesDisponibles = computed(() => [...new Set(budgets.value.map(b => b.type))])

// Remet la page à 1 quand on change un filtre
watch([selectedAnnee, selectedType], () => {
  currentPage.value = 1
})

const filteredBudgets = computed(() => {
  return budgets.value.filter(b => {
    const matchAnnee = selectedAnnee.value ? b.annee === selectedAnnee.value : true
    const matchType = selectedType.value ? b.type === selectedType.value : true
    return matchAnnee && matchType
  })
})

const totalPages = computed(() => Math.ceil(filteredBudgets.value.length / itemsPerPage))
const paginatedBudgets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredBudgets.value.slice(start, start + itemsPerPage)
})

function prevPage() {
  if (currentPage.value > 1) currentPage.value--
}
function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++
}
function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

function handleEdit(id) {
  router.push(`/modifier-budget/${id}`)
}

async function handleDelete(id) {
  if (confirm('Voulez-vous vraiment supprimer ce budget ?')) {
    try {
      await deleteBudget(id)
      budgets.value = budgets.value.filter(b => b.id !== id)
      alert('Budget supprimé avec succès.')
    } catch (e) {
      alert('Erreur lors de la suppression.')
      console.error(e)
    }
  }
}

const selectedFile = ref(null)

function handleFileChange(event) {
  selectedFile.value = event.target.files[0]
}

async function importerExcel() {
  if (!selectedFile.value) {
    alert("Veuillez sélectionner un fichier Excel à importer.")
    return
  }

  const isNewBudget = confirm("Voulez-vous créer un nouveau budget ?\nCliquez sur 'Annuler' pour choisir un budget existant.")

  let formData = new FormData()
  formData.append('file', selectedFile.value)

  if (isNewBudget) {
    const annee = prompt("Saisissez l'année du nouveau budget :", new Date().getFullYear())
    const type_budget = prompt("Saisissez le type du budget (exemple : depenses, recettes) :", "depenses")
    formData.append('annee', annee)
    formData.append('type_budget', type_budget)
  } else {
    const budgetId = prompt("Saisissez l'ID du budget existant dans lequel importer les données :")
    formData.append('budget_id', budgetId)
  }

  try {
    const response = await fetch('/api/import-budget/', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) throw new Error("Erreur lors de l'import.")

    const result = await response.json()
    alert(`✅ Import terminé avec succès. Prestataires importés :\n${result.lignes_importees.map(p => p.prestataire).join(', ')}`)

    await loadBudgets()
  } catch (error) {
    console.error(error)
  }
}

async function exporterExcel(annee, type) {
  try {
    const response = await fetch(`/api/export-budget/${annee}/${type}/`)
    if (!response.ok) throw new Error("Erreur lors de l'export")

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)

    const a = document.createElement('a')
    a.href = url
    a.download = `budget_${annee}_${type}.xlsx`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    alert("Impossible d'exporter le fichier Excel.")
    console.error(error)
  }
}
</script>

<style scoped>
.filters {
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filters label {
  font-weight: 500;
}

select {
  margin-left: 0.5rem;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-page {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  background-color: #2563eb;
  color: rgb(2, 2, 2);
  font-weight: 600;
  cursor: pointer;
}

.btn-page:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.btn-page.active {
  background-color: #1e40af;
  font-weight: 700;
  cursor: default;
}

.btn-export {
  background-color: #16a34a;
  color: white;
  padding: 0.3rem 0.6rem;
  margin-left: 0.4rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-export:hover {
  background-color: #15803d;
}

.btn-import {
  background-color: #eab308;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
}

.btn-import:hover {
  background-color: #ca8a04;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.btn-add {
  background-color: #2563eb;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: background-color 0.3s ease;
}

.btn-add:hover {
  background-color: #1e40af;
}
</style>

<style scoped src="@/assets/styles/TableList.css"></style>
