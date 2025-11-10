<template>
    <form @submit.prevent="submitForm" class="form-container">
        <h2>Enregistrer un Ordonnancement</h2>

        <!-- Champ de recherche -->
        <label>Rechercher une ligne :</label>
        <input type="text" v-model="searchQuery" placeholder="Ex : 2025 ou ACME SARL" />

        <label>Ligne Budgétaire :</label>
        <select v-model="form.ligne" required>
            <option value="" disabled>-- Sélectionner une ligne --</option>
            <option v-for="l in filteredLignes" :key="l.id" :value="l.id">
                {{ l.budget.annee }} - {{ l.prestataire.nom || l.prestataire.raison_sociale }}
            </option>
        </select>

        <p v-if="selectedLigne" class="budget-info">
            Budget disponible réel :
            <strong>{{ formatMontant(budgetDisponible) }} MAD</strong>
        </p>

        <label>Date :</label>
        <input type="date" v-model="form.date_ordonnancement" required />

        <label>Montant :</label>
        <input type="number" step="0.01" v-model.number="form.montant_ordonnancement" required />

        <label>Montant en lettres :</label>
        <textarea readonly rows="2" class="readonly-textarea" :value="montantEnLettres"></textarea>

        <label>Objet :</label>
        <input type="text" v-model="form.objet" required />

        <label>Justificatifs :</label>
        <textarea v-model="form.justificatifs" />

        <button type="submit" class="btn-submit">Créer</button>
    </form>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'

const lignes = ref([])
const selectedLigne = ref(null)
const searchQuery = ref('')

const form = ref({
    ligne: '',
    date_ordonnancement: '',
    montant_ordonnancement: null,
    objet: '',
    justificatifs: '',
    mode_paiement: 'virement',
})

async function loadLignes() {
    const res = await fetch('/api/ligne-budgetaire/')
    const allLignes = await res.json()

    lignes.value = allLignes.filter(ligne => {
        const budget = parseFloat(ligne.montant_budget_ttc || 0)
        const totalOrdo = parseFloat(ligne.total_ordonnancement || 0)
        return budget - totalOrdo > 0
    })
}
function formatMontant(montant) {
    return Number(montant || 0).toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

// ➤ Filtrer les lignes par recherche
const filteredLignes = computed(() => {
    if (!searchQuery.value) return lignes.value

    const query = searchQuery.value.toLowerCase()

    return lignes.value.filter(ligne => {
        const annee = String(ligne.budget.annee)
        const prestataire = (ligne.prestataire.nom || ligne.prestataire.raison_sociale || '').toLowerCase()
        return annee.includes(query) || prestataire.includes(query)
    })
})

watch(() => form.value.ligne, (ligneId) => {
    selectedLigne.value = lignes.value.find(l => l.id === ligneId) || null
})

// ➤ Conversion du montant
function convertirEnLettres(montant) {
    const unites = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf']
    const dizaines = ['', '', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt']

    function enLettres(n) {
        if (n === 0) return 'zéro'
        if (n < 20) return unites[n]
        if (n < 100) {
            const d = Math.floor(n / 10), u = n % 10
            let str = dizaines[d]
            if (d === 7 || d === 9) str += '-' + unites[10 + u]
            else if (u === 1 && d !== 8) str += ' et un'
            else if (u > 0) str += '-' + unites[u]
            return str
        }
        if (n < 1000) {
            const c = Math.floor(n / 100), r = n % 100
            let str = (c === 1 ? 'cent' : unites[c] + ' cent')
            if (r > 0) str += ' ' + enLettres(r)
            return str
        }
        if (n < 1000000) {
            const mil = Math.floor(n / 1000), r = n % 1000
            let str = (mil === 1 ? 'mille' : enLettres(mil) + ' mille')
            if (r > 0) str += ' ' + enLettres(r)
            return str
        }
        if (n < 1000000000) {
            const million = Math.floor(n / 1000000), r = n % 1000000
            let str = (million === 1 ? 'un million' : enLettres(million) + ' millions')
            if (r > 0) str += ' ' + enLettres(r)
            return str
        }
        return 'nombre trop grand'
    }

    const entier = Math.floor(montant)
    const centimes = Math.round((montant - entier) * 100)
    let texte = entier === 0 ? 'zéro dirham' : enLettres(entier) + ' dirham' + (entier > 1 ? 's' : '')
    if (centimes > 0) texte += ' et ' + enLettres(centimes) + ' centime' + (centimes > 1 ? 's' : '')
    return texte
}

const montantEnLettres = computed(() => convertirEnLettres(form.value.montant_ordonnancement || 0))

const budgetDisponible = computed(() => {
    if (!selectedLigne.value) return 0
    const budget = parseFloat(selectedLigne.value.montant_budget_ttc || 0)
    const totalOrdo = parseFloat(selectedLigne.value.total_ordonnancement || 0)
    return budget - totalOrdo
})

// ➤ Soumission du formulaire
async function submitForm() {
    if (
        !form.value.ligne ||
        !form.value.date_ordonnancement ||
        !form.value.montant_ordonnancement ||
        !form.value.objet
        
    ) {
        alert("Tous les champs obligatoires doivent être remplis.")
        return
    }

    if (form.value.montant_ordonnancement > budgetDisponible.value) {
        alert(`Dépassement ! Montant autorisé : ${budgetDisponible.value.toFixed(2)} MAD`)
        return
    }

    const res = await fetch('/api/ordonnancements/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value),
    })

    if (res.ok) {
        alert("Fiche créée avec succès")
        Object.assign(form.value, {
            ligne: '',
            date_ordonnancement: '',
            montant_ordonnancement: null,
            objet: '',
            justificatifs: '',
        })
        selectedLigne.value = null
    } else {
        const err = await res.json()
        alert("Erreur : " + JSON.stringify(err))
    }
}

onMounted(loadLignes)
</script>

<style scoped>
.form-container {
    max-width: 500px;
    margin: 2rem auto;
    background-color: #f9fafb;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

label {
    font-weight: 600;
}

input,
select,
textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1.8px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
}

.budget-info {
    color: #2563eb;
    font-style: italic;
}

.btn-submit {
    background-color: #2563eb;
    color: white;
    font-weight: 700;
    padding: 0.7rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.25s ease;
}

.btn-submit:hover {
    background-color: #1d4ed8;
}
</style>
