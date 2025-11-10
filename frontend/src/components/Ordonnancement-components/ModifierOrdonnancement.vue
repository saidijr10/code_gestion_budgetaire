<template>
    <div v-if="formLoaded" class="form-container">
        <h2>Modifier une Fiche d’Ordonnancement</h2>

        <form @submit.prevent="handleSubmit" novalidate>
            <label for="annee">Filtrer par année :</label>
            <input
                type="number"
                id="annee"
                v-model="anneeFiltre"
                @input="filterLignesParAnnee"
                placeholder="Ex: 2025"
            />

            <label for="ligne">Ligne Budgétaire :</label>
            <select id="ligne" v-model="form.ligne" required>
                <option disabled value="">-- Sélectionnez une ligne --</option>
                <option v-for="l in lignes" :key="l.id" :value="l.id">
                    {{ l.budget.annee }} - {{ l.prestataire.nom || l.prestataire.raison_sociale }}
                </option>
            </select>

            <label for="date_ordonnancement">Date d'ordonnancement :</label>
            <input type="date" id="date_ordonnancement" v-model="form.date_ordonnancement" required />

            <label for="montant_ordonnancement">Montant TTC :</label>
            <input
                type="number"
                step="0.01"
                id="montant_ordonnancement"
                v-model.number="form.montant_ordonnancement"
                placeholder="Ex: 1500.00"
                required
            />

            <label>Montant en lettres :</label>
            <textarea readonly rows="2" class="readonly-textarea" :value="montantEnLettres"></textarea>

            <label for="objet">Objet :</label>
            <input
                type="text"
                id="objet"
                v-model.trim="form.objet"
                placeholder="Ex: Règlement taxe professionnelle"
                required
            />

            <label for="justificatifs">Justificatifs :</label>
            <textarea
                id="justificatifs"
                v-model="form.justificatifs"
                placeholder="Informations supplémentaires"
                rows="3"
            ></textarea>

            <button type="submit" class="btn-submit">Modifier</button>

            <p v-if="generalError" class="error">{{ generalError }}</p>
        </form>
    </div>

    <p v-else class="loading">Chargement des données...</p>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const form = reactive({
    ligne: "",
    date_ordonnancement: "",
    montant_ordonnancement: null,
    objet: "",
    justificatifs: "",
});

const toutesLignes = ref([]);
const lignes = ref([]);
const anneeFiltre = ref('');
const formLoaded = ref(false);
const generalError = ref("");

// Nouveaux refs pour la vérification
const totalReglementLigne = ref(0);
const totalOrdonnancementLigne = ref(0);
const oldMontantOrdonnancement = ref(0);

// Charger toutes les lignes avec budget disponible > 0
async function loadLignes() {
    try {
        const res = await fetch("/api/ligne-budgetaire/");
        if (!res.ok) throw new Error("Erreur chargement lignes budgétaires");

        const allLignes = await res.json();

        toutesLignes.value = allLignes.filter(ligne => {
            const budget = parseFloat(ligne.montant_budget_ttc || 0);
            const totalOrdo = parseFloat(ligne.total_ordonnancement || 0);
            const totalReglement = parseFloat(ligne.total_reglement || 0);
            const budgetDispo = budget - totalOrdo - totalReglement;
            return budgetDispo > 0;
        });

        filterLignesParAnnee();
    } catch (e) {
        console.error(e);
    }
}

// Filtrer lignes selon l'année saisie
function filterLignesParAnnee() {
    if (!anneeFiltre.value) {
        lignes.value = toutesLignes.value;
    } else {
        lignes.value = toutesLignes.value.filter(l =>
            String(l.budget.annee).includes(anneeFiltre.value)
        );
    }
}

// Conversion du montant en lettres (français)
function convertirEnLettres(montant) {
    const unites = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix',
        'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf'];
    const dizaines = ['', '', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt'];

    function enLettres(n) {
        if (n === 0) return 'zéro';
        if (n < 20) return unites[n];
        if (n < 100) {
            const d = Math.floor(n / 10), u = n % 10;
            let str = dizaines[d];
            if (d === 7 || d === 9) str += '-' + unites[10 + u];
            else if (u === 1 && d !== 8) str += ' et un';
            else if (u > 0) str += '-' + unites[u];
            return str;
        }
        if (n < 1000) {
            const c = Math.floor(n / 100), r = n % 100;
            let str = (c === 1 ? 'cent' : unites[c] + ' cent');
            if (r > 0) str += ' ' + enLettres(r);
            return str;
        }
        if (n < 1000000) {
            const mil = Math.floor(n / 1000), r = n % 1000;
            let str = (mil === 1 ? 'mille' : enLettres(mil) + ' mille');
            if (r > 0) str += ' ' + enLettres(r);
            return str;
        }
        if (n < 1000000000) {
            const million = Math.floor(n / 1000000), r = n % 1000000;
            let str = (million === 1 ? 'un million' : enLettres(million) + ' millions');
            if (r > 0) str += ' ' + enLettres(r);
            return str;
        }
        return 'nombre trop grand';
    }

    const entier = Math.floor(montant);
    const centimes = Math.round((montant - entier) * 100);
    let texte = entier === 0 ? 'zéro dirham' : enLettres(entier) + ' dirham' + (entier > 1 ? 's' : '');
    if (centimes > 0) texte += ' et ' + enLettres(centimes) + ' centime' + (centimes > 1 ? 's' : '');
    return texte;
}
const montantEnLettres = computed(() => convertirEnLettres(form.montant_ordonnancement || 0));

// Charger la fiche ordonnancement existante
async function loadOrdonnancement() {
    try {
        const res = await fetch(`/api/ordonnancements/${route.params.id}/`);
        if (!res.ok) throw new Error("Erreur chargement ordonnancement");
        const data = await res.json();

        Object.assign(form, {
            ligne: data.ligne,
            date_ordonnancement: data.date_ordonnancement,
            montant_ordonnancement: parseFloat(data.montant_ordonnancement),
            objet: data.objet || "",
            justificatifs: data.justificatifs || "",
        });

        oldMontantOrdonnancement.value = parseFloat(data.montant_ordonnancement || 0);

        // Charger les infos de la ligne budgétaire associée
        if (data.ligne) {
            try {
                const ligneRes = await fetch(`/api/ligne-budgetaire/${data.ligne}/`);
                if (ligneRes.ok) {
                    const ligneData = await ligneRes.json();
                    totalReglementLigne.value = parseFloat(ligneData.total_reglement || 0);
                    totalOrdonnancementLigne.value = parseFloat(ligneData.total_ordonnancement || 0);
                }
            } catch (e) {
                console.error("Erreur chargement ligne budgétaire", e);
            }
        }

        formLoaded.value = true;
    } catch (e) {
        generalError.value = "Impossible de charger les données.";
        console.error(e);
    }
}

// Validation simple avant soumission
function validate() {
    generalError.value = "";
    if (!form.ligne) return generalError.value = "La ligne budgétaire est requise.", false;
    if (!form.date_ordonnancement) return generalError.value = "La date est requise.", false;
    if (!form.montant_ordonnancement || form.montant_ordonnancement <= 0) return generalError.value = "Le montant doit être supérieur à 0.", false;
    if (!form.objet.trim()) return generalError.value = "L'objet est requis.", false;
    return true;
}

// Soumission du formulaire
async function handleSubmit() {
    if (!validate()) return;

    // Vérification : le total ordonnancement recalculé ne doit pas être inférieur au total règlement
    const ancienMontant = oldMontantOrdonnancement.value;
    const nouveauMontant = form.montant_ordonnancement;
    const totalRecalcule = totalOrdonnancementLigne.value - ancienMontant + nouveauMontant;

    if (totalRecalcule < totalReglementLigne.value) {
        generalError.value = `Erreur : Le nouveau total des ordonnancements (${totalRecalcule.toLocaleString()} MAD) serait inférieur au total des règlements déjà effectués (${totalReglementLigne.value.toLocaleString()} MAD).`;
        return;
    }

    try {
        const res = await fetch(`/api/ordonnancements/${route.params.id}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form),
        });

        if (!res.ok) {
            const errData = await res.json();
            generalError.value = errData.detail || "Erreur lors de la modification.";
            return;
        }

        alert("Ordonnancement modifié avec succès !");
        router.push("/ordonnancements");
    } catch (e) {
        generalError.value = "Erreur lors de la modification.";
        console.error(e);
    }
}

onMounted(async () => {
    await loadLignes();
    await loadOrdonnancement();
});
</script>

<style scoped src="@/assets/styles/Form.css"></style>
