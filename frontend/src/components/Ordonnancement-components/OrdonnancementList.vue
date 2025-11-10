<template>
   <div class="container">
    <div class="header-actions">
      <h1 class="title">Liste des Ordonnancements</h1>
      <button class="btn-add" @click="goToAdd">Ajouter</button>
    </div>

    <!-- Recherche prestataire -->
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Rechercher un prestataire..."
      class="search-input"
    />

    <!-- Recherche budget -->
    <input
      type="text"
      v-model="searchBudget"
      placeholder="Rechercher par année ou type de budget..."
      class="search-input"
      style="margin-bottom: 1.5rem;"
    />

    <table class="ord-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Montant TTC</th>
          <th>Prestataire</th>
          <th>Budget</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ordo in paginatedOrdonnancements" :key="ordo.id">
          <td>{{ ordo.date_ordonnancement }}</td>
          <td>{{ formatMontant(ordo.montant_ordonnancement) }} DH</td>

          <td>{{ ordo.prestataire.nom || ordo.prestataire.raison_sociale }}</td>
          <td>{{ ordo.budget.annee }} - {{ ordo.budget.type }}</td>
          <td>
            <button @click="goToDetail(ordo.id)" class="btn-view">Afficher</button>
            <button @click="goToEdit(ordo.id)" class="btn-edit">Modifier</button>
            <button @click="deleteOrdo(ordo.id)" class="btn-delete">Supprimer</button>
          </td>
        </tr>
        <tr v-if="filteredOrdonnancements.length === 0">
          <td colspan="5" class="no-data">Aucun ordonnancement trouvé.</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-page">Précédent</button>
      <button
        v-for="page in totalPages"
        :key="page"
        @click="goToPage(page)"
        :class="['btn-page', { active: currentPage === page }]"
      >
        {{ page }}
      </button>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-page">Suivant</button>
    </div>

    <h2 class="subtitle">Totaux par prestataire et budget</h2>
    <table class="ord-table">
      <thead>
        <tr>
          <th>Prestataire</th>
          <th>Budget (Année - Type)</th>
          <th>Total Ordonnancement</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(montant, key) in totalParPrestataireBudget" :key="key">
          <td>{{ key.split('|')[0] }}</td>
          <td>{{ key.split('|')[1] }}</td>
          <td>{{ formatMontant(montant) }} DH</td>

        </tr>
      </tbody>
    </table>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const ordonnancements = ref([])
const error = ref('')
const searchTerm = ref('')
const searchBudget = ref('')
const router = useRouter()

const currentPage = ref(1)
const pageSize = 5

async function fetchOrdonnancements() {
  try {
    const res = await fetch('/api/ordonnancements/')
    if (!res.ok) throw new Error('Erreur lors du chargement')
    ordonnancements.value = await res.json()
  } catch (e) {
    error.value = 'Erreur de chargement des données'
    console.error(e)
  }
}

// Remet la page à 1 dès que les termes de recherche changent
watch([searchTerm, searchBudget], () => {
  currentPage.value = 1
})

// 🔍 Filtrage par prestataire et budget (année ou type)
const filteredOrdonnancements = computed(() => {
  const term = searchTerm.value.toLowerCase()
  const budgetTerm = searchBudget.value.toLowerCase()

  return ordonnancements.value.filter(o => {
    // Prestataire
    const nom = o.prestataire?.nom?.toLowerCase() || ''
    const raison = o.prestataire?.raison_sociale?.toLowerCase() || ''

    // Budget
    const annee = o.budget?.annee?.toString() || ''
    const type = o.budget?.type?.toLowerCase() || ''

    const prestataireMatch = nom.includes(term) || raison.includes(term)
    const budgetMatch = annee.includes(budgetTerm) || type.includes(budgetTerm)

    const prestataireOk = term ? prestataireMatch : true
    const budgetOk = budgetTerm ? budgetMatch : true

    return prestataireOk && budgetOk
  })
})

const totalParPrestataireBudget = computed(() => {
  const totals = {}

  for (const ordo of filteredOrdonnancements.value) {
    const prestataire = ordo.prestataire?.nom || ordo.prestataire?.raison_sociale || 'Inconnu'
    const budget = `${ordo.budget?.annee || ''} - ${ordo.budget?.type || ''}`
    const key = `${prestataire}|${budget}`

    if (!totals[key]) {
      totals[key] = 0
    }
    totals[key] += Number(ordo.montant_ordonnancement || 0)
  }

  return totals
})

const totalPages = computed(() => Math.ceil(filteredOrdonnancements.value.length / pageSize))

const paginatedOrdonnancements = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredOrdonnancements.value.slice(start, start + pageSize)
})
function formatMontant(montant) {
  return Number(montant || 0).toLocaleString('fr-FR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}


function goToDetail(id) {
  router.push(`/ordonnancements/${id}`)
}

function goToAdd() {
  router.push('/ordonnancements/ajouter') // adapte l'url selon ta route d'ajout
}

function goToEdit(id) {
  router.push(`/ordonnancements/${id}/edit`)
}

async function deleteOrdo(id) {
  if (!confirm('Voulez-vous vraiment supprimer cet ordonnancement ?')) return

  try {
    const res = await fetch(`/api/ordonnancements/${id}/`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Erreur suppression')
    ordonnancements.value = ordonnancements.value.filter(o => o.id !== id)

    if (currentPage.value > 1 && paginatedOrdonnancements.value.length === 0) {
      currentPage.value--
    }
  } catch (e) {
    alert('Erreur lors de la suppression.')
    console.error(e)
  }
}

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

onMounted(fetchOrdonnancements)
</script>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-add {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-add:hover {
  background-color: #1d4ed8;
}

.search-input {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Pagination */
.pagination {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-page {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  background-color: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-page:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.btn-page:not(:disabled):hover {
  background-color: #1e40af;
}

.btn-page.active {
  background-color: #1e40af;
  font-weight: 700;
  cursor: default;
}

.container {
  max-width: 1000px;
  margin: auto;
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.ord-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.ord-table th,
.ord-table td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
  font-size: 0.95rem;
}

.ord-table th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #374151;
}

.ord-table tr:hover {
  background-color: #f9fafb;
}

.btn-view,
.btn-edit,
.btn-delete {
  padding: 0.3rem 0.6rem;
  margin-right: 0.4rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-edit {
  background-color: #f59e0b;
  color: white;
}

.btn-view {
  background-color: #2563eb;
  color: white;
}

.btn-view:hover {
  background-color: #1e40af;
}

.btn-delete {
  background-color: #dc2626;
  color: white;
}

.btn-delete:hover {
  background-color: #991b1b;
}

.btn-edit:hover {
  background-color: #b45309;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
