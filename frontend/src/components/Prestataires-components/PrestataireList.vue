<template>
   <div class="container">

    <div class="header-actions">
      <h2 class="title">Liste des Prestataires</h2>
      <button class="btn-add" @click="goToAdd">Ajouter</button>
    </div>

    <!-- 🔍 Barre de recherche -->
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
          <th>Type</th>
          <th>Nom</th>
          <th>Prénom</th>
          <th>CIN</th>
          <th>Raison Sociale</th>
          <th>Adresse</th>
          <th>Téléphone</th>
          <th>Contact</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="presta in paginatedPrestataires" :key="presta.id">
          <td>{{ presta.type }}</td>
          <td>{{ presta.nom || '-' }}</td>
          <td>{{ presta.prenom || '-' }}</td>
          <td>{{ presta.cin || '-' }}</td>
          <td>{{ presta.raison_sociale || '-' }}</td>
          <td>{{ presta.adresse || '-' }}</td>
          <td>{{ presta.tel || '-' }}</td>
          <td>{{ presta.contact || '-' }}</td>
          <td>
            <div class="action-buttons">
              <button @click="handleEdit(presta)" class="btn-edit">Modifier</button>
              <button @click="handleDelete(presta.id)" class="btn-delete">Supprimer</button>
            </div>
          </td>

        </tr>
        <tr v-if="filteredPrestataires.length === 0">
          <td colspan="9" class="no-data">Aucun prestataire trouvé.</td>
        </tr>
      </tbody>
    </table>


<div class="pagination">
  <button
    @click="goToPage(currentPage - 1)"
    :disabled="currentPage === 1"
    class="pagination-btn"
  >
    «
  </button>

  <span class="pagination-number">{{ currentPage }}</span>

  <button
    @click="goToPage(currentPage + 1)"
    :disabled="currentPage === totalPages"
    class="pagination-btn"
  >
    »
  </button>
</div>




    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getPrestataires, deletePrestataire } from '@/Services/PrestaServices.js'
import { useRouter } from 'vue-router'

const prestataires = ref([])
const error = ref('')
const searchTerm = ref('')
const currentPage = ref(1)
const itemsPerPage = 5
const router = useRouter()

// Reset page à 1 dès que la recherche change
watch(searchTerm, () => {
  currentPage.value = 1
})

// Filtrage par recherche (nom, prénom ou raison sociale)
const filteredPrestataires = computed(() => {
  const term = searchTerm.value.toLowerCase()
  return prestataires.value.filter(p => {
    const nom = p.nom?.toLowerCase() || ''
    const prenom = p.prenom?.toLowerCase() || ''
    const raison = p.raison_sociale?.toLowerCase() || ''
    return nom.includes(term) || prenom.includes(term) || raison.includes(term)
  })
})

// Pagination sur liste filtrée
const paginatedPrestataires = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredPrestataires.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(filteredPrestataires.value.length / itemsPerPage))

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const goToAdd = () => {
  router.push('/ajout-pres')  // La route de ton formulaire d'ajout
}

async function loadPrestataires() {
  try {
    prestataires.value = await getPrestataires()
  } catch (e) {
    error.value = 'Erreur lors du chargement des prestataires.'
    console.error(e)
  }
}

function handleEdit(presta) {
  router.push(`/modifier/${presta.id}`)
}

async function handleDelete(id) {
  if (confirm('Es-tu sûr de vouloir supprimer ce prestataire ?')) {
    try {
      await deletePrestataire(id)
      prestataires.value = prestataires.value.filter(p => p.id !== id)
      alert('Prestataire supprimé avec succès.')
    } catch (e) {
      alert('Erreur lors de la suppression.')
      console.error(e)
    }
  }
}

onMounted(loadPrestataires)
</script>

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
.action-buttons {
  display: flex;
  gap: 0.5rem; /* espace horizontal entre les boutons */
}

.btn-edit,
.btn-delete {
  padding: 0.3rem 0.7rem;
  font-size: 0.85rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
}

.btn-edit {
  background-color: #facc15;
  color: black;
  border: none;
}

.btn-edit:hover {
  background-color: #eab308;
}

.btn-delete {
  background-color: #ef4444;
  color: white;
  border: none;
}

.btn-delete:hover {
  background-color: #dc2626;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.4rem;
  margin-top: 1rem;
}

/* Flèches pagination */
.pagination-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #d1d5db;
  background-color: white;
  border-radius: 6px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  color: #374151;
  transition: background-color 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Numéro de page */
.pagination-number {
  width: 30px;
  height: 30px;
  background-color: #2563eb;
  color: white;
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 1rem;
}

</style>

<style scoped src="@/assets/styles/TableList.css"></style>
