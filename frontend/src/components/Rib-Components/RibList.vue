<template>
  <div class="container">
    <!-- Ligne titre + bouton -->
    <div class="header-actions">
      <h2 class="title">Liste des RIBs</h2>
      <button class="btn-add" @click="goToAddRib">Ajouter</button>
    </div>

    <!-- 🔍 Champ de recherche -->
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Rechercher un prestataire..."
      class="search-input"
    />

    <!-- 📋 Tableau -->
    <table class="liste-table">
      <thead>
        <tr>
          <th>Prestataire</th>
          <th>RIB</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="rib in paginatedRibs" :key="rib.id">
          <td>{{ getPrestataireName(rib) }}</td>
          <td>{{ rib.rib }}</td>
          <td>
            <button class="btn-edit" @click="editRib(rib.id)">Modifier</button>
            <button class="btn-delete" @click="deleteRibItem(rib.id)">Supprimer</button>
          </td>
        </tr>
        <tr v-if="filteredRibs.length === 0">
          <td colspan="3" style="text-align: center;">Aucun RIB trouvé.</td>
        </tr>
      </tbody>
    </table>

    <!-- 📌 Pagination -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1" class="btn-page">«</button>
      <button
        v-for="page in totalPages"
        :key="page"
        @click="goToPage(page)"
        :class="['btn-page', { active: page === currentPage }]"
      >
        {{ page }}
      </button>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="btn-page">»</button>
    </div>

    <!-- ⚠️ Erreur -->
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getRibs, deleteRib } from '@/Services/RibServices.js'

const ribs = ref([])
const searchTerm = ref('')
const currentPage = ref(1)
const itemsPerPage = 5
const error = ref(null)
const router = useRouter()

// 🔄 Chargement initial
async function loadRibs() {
  error.value = null
  try {
    ribs.value = await getRibs()
  } catch (e) {
    error.value = e.message || 'Erreur lors du chargement des RIBs'
  }
}
onMounted(loadRibs)

// 🔁 Reset pagination à la page 1 à chaque modification de la recherche
watch(searchTerm, () => {
  currentPage.value = 1
})

const goToAddRib = () => {
  router.push({ name: 'RibAdd' })
}
// 🔍 Filtrage des RIBs par nom, prénom ou raison sociale
const filteredRibs = computed(() => {
  const term = searchTerm.value.toLowerCase()
  if (!term) return ribs.value

  return ribs.value.filter(rib => {
    const info = rib.prestataire_info
    const nom = info?.nom?.toLowerCase() || ''
    const prenom = info?.prenom?.toLowerCase() || ''
    const raison = info?.raison_sociale?.toLowerCase() || ''
    return nom.includes(term) || prenom.includes(term) || raison.includes(term)
  })
})

// 📄 Pagination
const totalPages = computed(() => Math.ceil(filteredRibs.value.length / itemsPerPage))
const paginatedRibs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredRibs.value.slice(start, start + itemsPerPage)
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

// 🔁 Obtenir nom ou raison sociale du prestataire
function getPrestataireName(rib) {
  const info = rib.prestataire_info
  if (!info) return 'Inconnu'
  if (info.type === 'physique') {
    return `${info.nom || ''} ${info.prenom || ''}`.trim() || 'Inconnu'
  } else if (info.type === 'morale') {
    return info.raison_sociale || 'Inconnu'
  }
  return 'Inconnu'
}

// 📝 Modifier
function editRib(id) {
  router.push({ name: 'ModifierRib', params: { id } })
}

// ❌ Supprimer
async function deleteRibItem(id) {
  if (!confirm('Confirmez-vous la suppression de ce RIB ?')) return
  error.value = null
  try {
    await deleteRib(id)
    await loadRibs()

    // Ajuster la page si suppression du dernier élément visible
    if (paginatedRibs.value.length === 0 && currentPage.value > 1) {
      currentPage.value -= 1
    }
  } catch (e) {
    error.value = e.message || 'Erreur lors de la suppression'
  }
}
</script>

<style scoped src="@/assets/styles/TableList.css"></style>
<style scoped>
.search-input {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 8px;
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
</style>
