<template>
 <div class="container">

    <!-- Entête avec titre et bouton Ajouter -->
    <div class="header-actions">
      <h2 class="title">Liste des Lignes Budgétaires (Dépenses)</h2>
      <button class="btn-add" @click="router.push('/LigneBudgetaire/add')">Ajouter</button>
    </div>

    <!-- 🔍 Champ de recherche prestataire -->
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Rechercher un prestataire..."
      class="search-input"
    />

    <!-- 🔍 Champ de recherche année budget -->
    <input
      type="number"
      v-model="searchYear"
      placeholder="Rechercher par année de budget..."
      class="search-input"
      min="1900"
      max="2100"
    />

    <table class="liste-table">
      <thead>
        <tr>
          <th>Budget (Année)</th>
          <th>Rubrique</th>
          <th>Sous-rubrique</th>
          <th>Prestataire</th>
          <th>Montant budget TTC</th>
          <th>Montant totales ordonnacés</th>
          <th>Montant totales reglé</th>

          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ligne in paginatedLignes" :key="ligne.id">
          <td>{{ ligne.budget.annee }}</td>
          <td>{{ isValidText(ligne.rubrique) ? ligne.rubrique : '-' }}</td>
          <td>{{ isValidText(ligne.sous_rubrique) ? ligne.sous_rubrique : '-' }}</td>


          <td>
            {{ ligne.prestataire.nom
              ? ligne.prestataire.nom + ' ' + (ligne.prestataire.prenom || '')
              : (ligne.prestataire.raison_sociale || 'N/A') }}
          </td>
          <td class="text-right">
            {{ formatMontant(ligne.montant_budget_ttc) }}
          </td>
          <td class="text-right">
            {{ formatMontant(ligne.total_ordonnancement) }}
          </td>
          <td class="text-right">
            {{ formatMontant(ligne.total_reglement) }}
          </td>
          <td>
            <div class="action-buttons">
              <button @click="editLigne(ligne.id)" class="btn-edit">Modifier</button>
              <button @click="deleteLigne(ligne.id)" class="btn-delete">Supprimer</button>
            </div>
          </td>

        </tr>
        <tr v-if="filteredLignes.length === 0">
          <td colspan="4" class="no-data">Aucune ligne budgétaire trouvée.</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
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

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const lignes = ref([])
const error = ref('')
const router = useRouter()

const searchTerm = ref('')
const searchYear = ref('')

const currentPage = ref(1)
const itemsPerPage = 5

// Recharge la page 1 quand on change recherche
watch([searchTerm, searchYear], () => {
  currentPage.value = 1
})

// Chargement initial des lignes budgétaires
async function loadLignes() {
  try {
    const res = await fetch('/api/ligne-budgetaire/')
    if (!res.ok) throw new Error('Erreur réseau')
    lignes.value = await res.json()
  } catch (e) {
    error.value = "Erreur lors du chargement des lignes budgétaires."
    console.error(e)
  }
}

// Filtrage par prestataire et année budget
const filteredLignes = computed(() => {
  const term = searchTerm.value.toLowerCase()
  const year = searchYear.value

  return lignes.value.filter(ligne => {
    const p = ligne.prestataire
    const nom = p?.nom?.toLowerCase() || ''
    const prenom = p?.prenom?.toLowerCase() || ''
    const raison = p?.raison_sociale?.toLowerCase() || ''

    const prestataireMatch = !term || nom.includes(term) || prenom.includes(term) || raison.includes(term)
    const yearMatch = !year || ligne.budget?.annee?.toString() === year.toString()

    return prestataireMatch && yearMatch
  })
})

// Pagination
const totalPages = computed(() => Math.ceil(filteredLignes.value.length / itemsPerPage))

const paginatedLignes = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredLignes.value.slice(start, start + itemsPerPage)
})
function formatMontant(montant) {
  return Number(montant || 0).toLocaleString('fr-FR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
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

// Modifier / Supprimer
function editLigne(id) {
  router.push(`/ligne-budgetaire/modifier/${id}`)
}
function isValidText(value) {
  return typeof value === 'string' && value.trim() !== '' && value !== 'nan'
}

async function deleteLigne(id) {
  if (!confirm('Voulez-vous vraiment supprimer cette ligne budgétaire ?')) return

  try {
    const res = await fetch(`/api/ligne-budgetaire/${id}/`, {
      method: 'DELETE',
    })
    if (res.ok) {
      lignes.value = lignes.value.filter(l => l.id !== id)
      alert('Ligne budgétaire supprimée.')
    } else {
      throw new Error('Erreur suppression')
    }
  } catch (e) {
    error.value = "Erreur lors de la suppression."
    console.error(e)
  }
}

onMounted(loadLignes)
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
.action-buttons {
  display: flex;
  gap: 0.5rem; /* Espace entre les boutons */
  justify-content: center;
  align-items: center;
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
  color: rgb(45, 18, 248);
  font-weight: 600;
  cursor: pointer;
}

.btn-page:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.btn-page.active {
  background-color: #1e40af;
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
