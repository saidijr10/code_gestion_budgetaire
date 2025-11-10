<template>
    <div class="fiche-container  fiche-a-imprimer" v-if="ordo">
        <h1 class="title">Fiche d’Ordonnancement</h1>

        <section class="fiche-content">
            <p><strong>Date :</strong> {{ ordo.date_ordonnancement }}</p>
            <p><strong>OBJET :</strong> {{ ordo.objet }}</p>
            <p><strong>BÉNÉFICIAIRE :</strong>
                {{
                    ordo.prestataire?.nom
                    || ordo.prestataire?.raison_sociale
                    || ordo.prestataire
                    || 'Non défini'
                }}
            </p>
            <p><strong>MONTANT :</strong> {{ formatMontant(ordo.montant_ordonnancement) }} DH</p>


            <p><strong>MODE DE PAIEMENT :</strong> {{ formatModePaiement(ordo.mode_paiement) }}</p>
            <p><strong>IDENTITÉ BANCAIRE :</strong> {{ ordo.rib || 'Non défini' }}</p>
            <p><strong>JUSTIFICATIFS :</strong> {{ ordo.justificatifs || 'Aucun' }}</p>

            <p><strong>Le présent ordre est arrété a la somme de :</strong> {{ montantEnLettres }}</p>

            <hr class="divider" />

            <table class="visas-table">
                <thead>
                    <tr>
                        <th> </th>
                        <th class="visas-col-header">Comptabilité</th>
                        <th class="visas-col-header">Budget</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>VISAS</td>
                        <td></td>
                        <td></td>
                    </tr>
                </tbody>
            </table>



            <hr class="divider" />

        </section>

        <hr class="divider" />

        <div class="signataires">
            <div class="signataire">
                <p><strong>Signataire 1</strong></p>
                <div class="signature-placeholder">Signature</div>
            </div>
            <div class="signataire">
                <p><strong>Signataire 2</strong></p>
                <div class="signature-placeholder">Signature</div>
            </div>
        </div>

        <!-- Lien de retour -->
        <router-link to="/ordonnancements" class="btn-back">← Retour à la liste</router-link>
        <button @click="imprimerFiche" class="btn-export">
            Imprimer cette fiche
        </button>

    </div>

    <p v-else class="loading">Chargement de la fiche...</p>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const ordo = ref(null)
const route = useRoute()

async function fetchOrdonnancement() {
    try {
        const res = await fetch(`/api/ordonnancements/${route.params.id}/`)
        if (!res.ok) throw new Error('Erreur chargement fiche')
        ordo.value = await res.json()
    } catch (e) {
        console.error(e)
    }
}

function formatModePaiement(mode) {
    if (mode === 'virement') return 'Virement'
    if (mode === 'cheque') return 'Chèque'
    if (mode === 'espece') return 'Espèce'
    return mode
}

function imprimerFiche() {
    window.print()
}
// Fonction pour convertir en lettres
function convertirEnLettres(montant) {
    const unites = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
        "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"];
    const dizaines = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante", "quatre-vingt", "quatre-vingt"];

    function enLettres(n) {
        if (n === 0) return "zéro";
        if (n < 20) return unites[n];

        if (n < 100) {
            const d = Math.floor(n / 10);
            const u = n % 10;
            let str = dizaines[d];
            if (d === 7 || d === 9) {
                str += "-" + unites[10 + u];
            } else if (u === 1 && d !== 8) {
                str += " et un";
            } else if (u > 0) {
                str += "-" + unites[u];
            }
            return str;
        }

        if (n < 1000) {
            const c = Math.floor(n / 100);
            const r = n % 100;
            let str = (c === 1 ? "cent" : unites[c] + " cent");
            if (r > 0) str += " " + enLettres(r);
            return str;
        }

        if (n < 1000000) {
            const mil = Math.floor(n / 1000);
            const r = n % 1000;
            let str = (mil === 1 ? "mille" : enLettres(mil) + " mille");
            if (r > 0) str += " " + enLettres(r);
            return str;
        }

        if (n < 1000000000) {
            const million = Math.floor(n / 1000000);
            const r = n % 1000000;
            let str = (million === 1 ? "un million" : enLettres(million) + " millions");
            if (r > 0) str += " " + enLettres(r);
            return str;
        }

        return "nombre trop grand";
    }

    const entier = Math.floor(montant);
    const centimes = Math.round((montant - entier) * 100);
    let texte = entier === 0 ? "zéro dirham" : enLettres(entier) + " dirham" + (entier > 1 ? "s" : "");
    if (centimes > 0) {
        texte += " et " + enLettres(centimes) + " centime" + (centimes > 1 ? "s" : "");
    }
    return texte;
}

const montantEnLettres = computed(() => {
    return convertirEnLettres(ordo.value?.montant_ordonnancement || 0)
})
function formatMontant(montant) {
    return Number(montant || 0).toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}


onMounted(fetchOrdonnancement)
</script>

<style scoped>
.fiche-container {
    max-width: 700px;
    margin: auto;
    background: #fff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', sans-serif;
}

.title {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    color: #1e293b;
    font-weight: bold;
    text-align: center;
}

.fiche-content p {
    margin: 0.6rem 0;
    font-size: 1rem;
    color: #374151;
}

.divider {
    margin: 1.5rem 0;
    border-top: 1px solid #e5e7eb;
}

.btn-back {
    display: inline-block;
    margin-top: 2rem;
    padding: 0.5rem 1rem;
    background-color: #e0e7ff;
    color: #1d4ed8;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    transition: background-color 0.2s ease;
}

.btn-back:hover {
    background-color: #c7d2fe;
}

.loading {
    text-align: center;
    font-size: 1.1rem;
    margin-top: 3rem;
}

.signataires {
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
}

.signataire {
    width: 45%;
    text-align: center;
    font-weight: 600;
    color: #334155;
}

.signature-placeholder {
    margin-top: 3rem;
    border: 2px solid #9ca3af;
    height: 100px;
    border-radius: 6px;
    background-color: #f3f4f6;
    line-height: 100px;
    color: #9ca3af;
    font-style: italic;
    user-select: none;
}

.visas-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2rem;
    font-size: 1rem;
    border: 1px solid #cbd5e1;
}

.visas-table th,
.visas-table td {
    border: 1px solid #cbd5e1;
    padding: 0.75rem;
    text-align: center;
}

.visas-label {
    width: 20%;
    background-color: #f1f5f9;
    font-weight: bold;
    text-align: left;
}

.visas-col {
    width: 40%;
    background-color: #f9fafb;
}
</style>

<style>
@media print {

    /* Masquer tout sauf la fiche */
    body * {
        visibility: hidden !important;
    }

    .fiche-a-imprimer,
    .fiche-a-imprimer * {
        visibility: visible !important;
    }

    .fiche-a-imprimer {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        box-shadow: none;
        border: none;
    }

    /* Masquer les boutons et liens */
    .btn-export,
    .btn-back {
        display: none !important;
    }

    .app-nav {
        display: none !important;
    }
}
</style>