<template>
  <div>
    <div class="header-actions">
      <h2 class="title">Liste des Règlements</h2>
      <button class="btn-add" @click="goToAdd">Ajouter</button>
    </div>

    <!-- Barre de recherche -->
    <input
      type="text"
      v-model="searchTerm"
      placeholder="Rechercher un règlement..."
      class="search-input"
    />

    <table class="liste-table">
      <thead>
        <tr>
          <th>Prestataire</th>
          <th>Date paiement</th>
          <th>Montant réglé</th>
          <th>mode_paiement</th>
          <th>Compte débité</th>
          <th>reference_cheque</th>
          <th>Règlement relatif à</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in paginatedReglements" :key="r.id">
          <td>{{ r.ligne?.prestataire?.nom || r.ligne?.prestataire?.raison_sociale || '-' }}</td>
          <td>{{ r.date_paiement }}</td>
          <td class="text-right">{{ formatMontant(r.montant_regler) }}</td>
          <td>{{ r.mode_paiement || '-' }}</td>
          <!-- Compte débité -->
          <td>
            {{
              r.mode_paiement?.toLowerCase() === 'virement'
                ? (r.compte_debite || '-')
                : '-'
            }}
          </td>

          <!-- Référence chèque -->
          <td>
            {{
              r.mode_paiement?.toLowerCase() === 'cheque'
                ? (r.ref_cheque || '-')
                : '-'
            }}
          </td>

          <td>{{ r.reglement_rel || '-' }}</td>
         
          <td>
            <div class="actions-group">
              <button class="btn-view" @click="showReglement(r.id)">Afficher</button>
              <button class="btn-edit" @click="editReglement(r.id)">Modifier</button>
              <button class="btn-delete" @click="deleteReglement(r.id)">Supprimer</button>
            </div>
          </td>
        </tr>
        <tr v-if="filteredReglements.length === 0">
          <td colspan="7" class="no-data">Aucun règlement trouvé.</td>
        </tr>
      </tbody>
    </table> 

    <div class="pagination">
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">«</button>
      <button
        v-for="page in totalPages"
        :key="page"
        :class="{ active: page === currentPage }"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>
      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">»</button>
    </div>

    <h2 class="subtitle">Totaux par ligne budgétaire</h2>
    <table class="liste-table">
      <thead>
        <tr>
          <th>Ligne budgétaire</th>
          <th>Prestataire</th>
          <th>Total Règlement</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(montant, key) in totalParLigneEtPrestataire" :key="key">
          <td>{{ key.split(' | ')[0] }}</td>
          <td>{{ key.split(' | ')[1] }}</td>
          <td>{{ formatMontant(montant) }} DH</td>

        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const reglements = ref([])
const searchTerm = ref('')
const currentPage = ref(1)
const itemsPerPage = 5

// Reset page à 1 quand on modifie la recherche
watch(searchTerm, () => {
  currentPage.value = 1
})

const filteredReglements = computed(() => {
  if (!searchTerm.value) return reglements.value

  const term = searchTerm.value.toLowerCase()
  return reglements.value.filter(r => {
    const nom = r.ligne?.prestataire?.nom?.toLowerCase() || ''
    const raison = r.ligne?.prestataire?.raison_sociale?.toLowerCase() || ''
    return nom.includes(term) || raison.includes(term)
  })
})

const paginatedReglements = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredReglements.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(filteredReglements.value.length / itemsPerPage))

const totalParLigneEtPrestataire = computed(() => {
  const totals = {}

  for (const reglement of filteredReglements.value) {
    const ligne = reglement.ligne
    if (!ligne) continue

    const prestataire = reglement.ligne?.prestataire?.nom || reglement.ligne?.prestataire?.raison_sociale || 'Prestataire inconnu'

    const key = `${ligne.id} - ${ligne.nom || ligne.numero || 'Ligne inconnue'} | ${prestataire}`

    if (!totals[key]) totals[key] = 0
    totals[key] += Number(reglement.montant_regler || 0)
  }

  return totals
})

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page
}

async function loadReglements() {
  try {
    const res = await fetch('/api/reglements/')
    if (!res.ok) throw new Error('Erreur de chargement')
    reglements.value = await res.json()
  } catch (error) {
    alert('Erreur lors du chargement des règlements')
  }
}
function formatMontant(montant) {
  if (!montant) return '0,00'

  return Number(montant).toLocaleString('fr-FR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}


function editReglement(id) {
  router.push(`/reglements/modifier/${id}`)
}

function showReglement(id) {
  router.push(`/reglements/${id}`)
}

async function deleteReglement(id) {
  if (!confirm(`Voulez-vous vraiment supprimer le règlement ${id} ?`)) return

  const res = await fetch(`/api/reglements/${id}/`, { method: 'DELETE' })

  if (res.ok) {
    reglements.value = reglements.value.filter(r => r.id !== id)
    alert('Règlement supprimé')

    // Ajuste la page si on supprime le dernier élément visible
    if (paginatedReglements.value.length === 0 && currentPage.value > 1) {
      currentPage.value -= 1
    }
  } else {
    alert('Erreur lors de la suppression')
  }
}

function goToAdd() {
  router.push('/reglements/ajouter') // adapte l'URL d'ajout selon ta route
}

onMounted(loadReglements)
</script>

<style scoped>
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

.search-input {
  margin-bottom: 1rem;
  padding: 0.5rem 1rem;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Optionnel : tu peux ajouter tes styles de pagination et table ici ou dans ta feuille TableList.css */
</style>

<style scoped src="@/assets/styles/TableList.css"></style>
