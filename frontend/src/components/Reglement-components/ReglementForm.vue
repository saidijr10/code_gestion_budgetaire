<template>
    <form @submit.prevent="submitForm" class="form-container">
        <h2>Enregistrer un Règlement</h2>
        <!-- Champ recherche libre -->
        <label>Rechercher Ligne Budgétaire (année ou nom prestataire) :</label>
        <input
            type="text"
            v-model="searchLigne"
            placeholder="Ex: 2025 ou Dupont"
            class="search-input"
        />

        <label>Ligne Budgétaire :</label>
        <select v-model="form.ligne" required>
            <option value="" disabled>-- Sélectionner une ligne --</option>
            <option v-for="l in filteredLignes" :key="l.id" :value="l.id">
                {{ l.budget.annee }} - {{ l.prestataire.nom || l.prestataire.raison_sociale }}
            </option>
        </select>

        <p v-if="ordonnancement" class="budget-info">
            Montant ordonnancement :
            <strong>{{ formatMontant(ordonnancement.montant_ordonnancement) }} MAD</strong>
        </p>

        <p v-if="selectedLigne" class="budget-info">
            Budget disponible :
            <strong>{{ formatMontant(budgetDisponible) }} MAD</strong>
        </p>

        <label>Date de paiement :</label>
        <input type="date" v-model="form.date_paiement" required />

        <label>Montant réglé (MAD) :</label>
        <input type="number" step="0.01" v-model.number="form.montant_regler" required />

        <label>Montant en lettres :</label>
        <textarea readonly rows="2" class="readonly-textarea" :value="montantEnLettres"></textarea>

        <label>Mode de paiement :</label>
        <select v-model="form.mode_paiement" required>
            <option disabled value="">-- Sélectionner un mode --</option>
            <option value="virement">Virement</option>
            <option value="cheque">Chèque</option>
            <option value="espece">Espèce</option>
        </select>

        <!-- Affichage conditionnel selon mode_paiement -->
        <div v-if="form.mode_paiement === 'virement'">
            <label>Compte débité :</label>
            <input type="text" v-model.trim="form.compte_debite" :class="{ error: errors.compte_debite }" required />
            <p v-if="errors.compte_debite" class="error">{{ errors.compte_debite }}</p>
        </div>

        <div v-if="form.mode_paiement === 'cheque'">
            <label>Référence chèque :</label>
            <input type="text" v-model.trim="form.ref_cheque" required />
        </div>

        <label>Justification :</label>
        <textarea v-model.trim="form.justification"></textarea>

        <label>Règlement relatif à :</label>
        <input type="text" v-model.trim="form.reglement_rel" required />

        <button type="submit" class="btn-submit">Enregistrer le règlement</button>
    </form>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

const lignes = ref([])
const ordonnancements = ref([])
const selectedLigne = ref(null)
const ordonnancement = ref(null)

const form = ref({
    ligne: '',
    date_paiement: '',
    montant_regler: null,
    justification: '',
    compte_debite: '',
    reglement_rel: '',
    mode_paiement: '',
    ref_cheque: '',
})

const searchLigne = ref('')

const filteredLignes = computed(() => {
    const filtered = lignes.value.filter(ligne => {
        const ord = parseFloat(ligne.total_ordonnancement || 0)
        const totalRegl = parseFloat(ligne.total_reglement || 0)
        return (ord - totalRegl) > 0
    })

    if (!searchLigne.value.trim()) return filtered

    const s = searchLigne.value.toLowerCase()
    return filtered.filter(l => {
        const anneeStr = String(l.budget.annee)
        const nomPrest = (l.prestataire.nom || l.prestataire.raison_sociale || '').toLowerCase()
        return anneeStr.includes(s) || nomPrest.includes(s)
    })
})

const errors = reactive({ compte_debite: '' })

function clearErrors() {
    Object.keys(errors).forEach(key => (errors[key] = ''))
}

function formatMontant(montant) {
    return Number(montant || 0).toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}


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

const montantEnLettres = computed(() => {
    return convertirEnLettres(form.value.montant_regler || 0)
})

const budgetDisponible = computed(() => {
    if (!selectedLigne.value) return 0
    const total = selectedLigne.value.montant_budget_ttc || 0
    const reg = selectedLigne.value.total_reglement || 0
    return total - reg
})

async function loadLignes() {
    const res = await fetch('/api/ligne-budgetaire/')
    if (res.ok) lignes.value = await res.json()
}

async function loadOrdonnancements() {
    const res = await fetch('/api/ordonnancements/')
    if (res.ok) ordonnancements.value = await res.json()
}

watch(() => form.value.ligne, (ligneId) => {
    selectedLigne.value = filteredLignes.value.find(l => l.id === ligneId) || null

    if (selectedLigne.value) {
        const totalOrdo = Number(selectedLigne.value.total_ordonnancement || 0)
        const totalRegl = Number(selectedLigne.value.total_reglement || 0)
        ordonnancement.value = {
            montant_ordonnancement: totalOrdo - totalRegl
        }
    } else {
        ordonnancement.value = null
    }
})

function isValidCompteDebite(compte) {
    const regex = /^\d{11,16}$/
    return regex.test(compte)
}

async function submitForm() {
    clearErrors()

    if (
        !form.value.ligne ||
        !form.value.date_paiement ||
        !form.value.montant_regler ||
        !form.value.mode_paiement ||
        !form.value.reglement_rel.trim()
    ) {
        alert('Veuillez remplir tous les champs obligatoires.')
        return
    }

    if (form.value.mode_paiement === 'virement') {
        if (!form.value.compte_debite.trim()) {
            errors.compte_debite = 'Le compte débité est obligatoire pour le virement.'
            return
        }
        if (!isValidCompteDebite(form.value.compte_debite.trim())) {
            errors.compte_debite = 'Le numéro de compte doit contenir entre 11 et 16 chiffres.'
            return
        }
    }

    if (form.value.mode_paiement === 'cheque') {
        if (!form.value.ref_cheque.trim()) {
            alert('La référence chèque est obligatoire pour le paiement par chèque.')
            return
        }
    }

    if (selectedLigne.value) {
        const totalOrdo = Number(selectedLigne.value.total_ordonnancement || 0)
        const totalRegl = Number(selectedLigne.value.total_reglement || 0)
        ordonnancement.value = {
            montant_ordonnancement: totalOrdo - totalRegl
        }
    } else {
        ordonnancement.value = null
    }

    if (form.value.montant_regler > (ordonnancement.value?.montant_ordonnancement || 0)) {
        alert(`Le montant réglé (${form.value.montant_regler} MAD) dépasse le montant d'ordonnancement disponible (${(ordonnancement.value.montant_ordonnancement).toFixed(2)} MAD).`)
        return
    }

    const payload = {
        ...form.value,
        ligne_id: Number(form.value.ligne),
        montant_regler: Number(form.value.montant_regler),
        compte_debite: form.value.compte_debite.trim(),
        justification: form.value.justification.trim(),
        reglement_rel: form.value.reglement_rel.trim(),
        mode_paiement: form.value.mode_paiement,
        ref_cheque: form.value.ref_cheque.trim(),
    }

    delete payload.ligne

    try {
        const res = await fetch('/api/reglements/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })

        if (res.ok) {
            alert('Règlement enregistré avec succès')
            Object.assign(form.value, {
                ligne: '',
                date_paiement: '',
                montant_regler: null,
                justification: '',
                compte_debite: '',
                reglement_rel: '',
                mode_paiement: '',
                ref_cheque: '',
            })
            selectedLigne.value = null
            ordonnancement.value = null
        } else {
            const errData = await res.json()
            alert("Erreur lors de l'enregistrement du règlement : " + (errData.detail || JSON.stringify(errData)))
        }
    } catch (error) {
        alert('Erreur réseau : ' + error.message)
    }
}

onMounted(() => {
    loadLignes()
    loadOrdonnancements()
})
</script>

<style scoped>
.form-container {
    max-width: 500px;
    margin: 2rem auto;
    background-color: #f9fafb;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1f2937;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

label {
    font-weight: 600;
    margin-bottom: 0.3rem;
    display: block;
}

input,
select,
textarea {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1.8px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.2s ease;
    font-family: inherit;
    resize: vertical;
}

input.error {
    border-color: #dc2626;
    box-shadow: 0 0 5px #dc2626;
}

input:focus,
select:focus,
textarea:focus {
    border-color: #3b82f6;
    outline: none;
    box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
}

textarea {
    min-height: 80px;
}

.readonly-textarea {
    background-color: #f3f4f6;
    color: #374151;
    resize: none;
}

.prestataire-info p,
.budget-info {
    font-style: italic;
    color: #2563eb;
}

.btn-submit {
    background-color: #2563eb;
    color: white;
    font-weight: 700;
    padding: 0.7rem 1rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.1rem;
    transition: background-color 0.25s ease;
    margin-top: 1rem;
}

.btn-submit:hover {
    background-color: #1d4ed8;
}

.error {
    color: #dc2626;
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

.search-input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    margin-bottom: 1rem;
    border: 1.8px solid #cbd5e1;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
}
</style>
