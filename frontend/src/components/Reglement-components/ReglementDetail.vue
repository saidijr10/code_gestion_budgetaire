<template>
    <div class="detail-container fiche-a-imprimer" v-if="reglement">
        <h3 class="header">Monsieur le Directeur de <br />L’Agence Grands Comptes Rabat</h3>

        <p><strong>Objet :</strong> Ordre de Virement</p>

        <p>Monsieur le Directeur ;</p>

       <p v-if="reglement.mode_paiement === 'virement'">
            Veuillez, par le débit de notre compte n°{{ compte_debite }}
        </p>
        <p v-if="reglement.mode_paiement === 'virement'">
            , virer :
        </p>
        <p v-else-if="reglement.mode_paiement === 'cheque'">
        Veuillez procéder au paiement par chèque (réf. : {{ reglement.ref_cheque || 'N/A' }})
        </p>
        <p v-else-if="reglement.mode_paiement === 'espece'">
        Veuillez procéder au paiement en espèces
        </p>
        <p v-else>
        Mode de paiement non spécifié
        </p>

        <p><strong>A :</strong> {{ prestataireNom }}</p>

        <p>
            La somme : <strong>{{ montantFormatte }}</strong>(<em>{{ montantEnLettres }}</em>).
        </p>

        <p><strong>Au Compte (RIB) :</strong> {{ rib }}</p>

        <p><strong>Domiciliation :</strong> {{ domiciliation }}</p>


        <p>Relatif au règlement de :</p>
        <ul>
            <li>{{ reglement.reglement_rel || '-' }}</li>
        </ul>

        <div class="signataires">
            <div class="signataire">Signataire 2</div>
            <div class="signataire signataire-1">Signataire 1</div>
        </div>
        <button @click="imprimer" class="btn-export">Imprimer</button>
    </div>

    <p v-else>Chargement des données...</p>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

function imprimer() {
    window.print();
}
const route = useRoute()
const reglementId = Number(route.params.id)

const reglement = ref(null)

async function loadReglement() {
    const res = await fetch(`/api/reglements/${reglementId}/`)
    if (res.ok) {
        reglement.value = await res.json()
    } else {
        alert("Erreur lors du chargement du règlement")
    }
}const rib = computed(() => {
    if (!reglement.value) return ''
    return reglement.value.ligne.rib || ''
})

const domiciliation = computed(() => {
    if (!reglement.value) return ''
    return reglement.value.ligne.domiciliation || ''
})

const compte_debite = computed(() => {
    if (!reglement.value) return ''
    return reglement.value.compte_debite || ''
})

const prestataireNom = computed(() => {
    if (!reglement.value) return ''
    const p = reglement.value.ligne.prestataire
    if (!p) return ''
    return p.nom || p.raison_sociale || ''
})

const montantFormatte = computed(() => {
    if (!reglement.value) return ''
    return Number(reglement.value.montant_regler).toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })
})
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
    return convertirEnLettres(reglement.value?.montant_regler || 0)
})


onMounted(loadReglement)
</script>

<style scoped>
.detail-container {
    max-width: 600px;
    margin: 2rem auto;
    font-family: 'Times New Roman', serif;
    font-size: 1.1rem;
    color: #1f2937;
    line-height: 1.6;
    background: #fff;
    padding: 2rem;
    border: 1px solid #ddd;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.1);
}

.header {
    font-weight: 700;
    font-size: 1.3rem;
    margin-bottom: 1rem;
    text-align: right;
    /* <-- ici */
}


ul {
    list-style: inside disc;
    margin-left: 1rem;
    margin-bottom: 2rem;
}

.signataires {
    display: flex;
    justify-content: space-between;
    margin-top: 4rem;
}

.signataire {
    font-weight: 600;
    border-top: 1px solid #000;
    width: 30%;
    text-align: center;
    padding-top: 0.5rem;
    user-select: none;
}

.signataire-1 {
    margin-left: auto;
}
</style>
<style>
@media print {
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

    /* Cacher l'entête/menu de App.vue */
    .app-nav {
        display: none !important;
    }

    /* Cacher les boutons s’il y en a */
    .btn-export,
    .btn-back {
        display: none !important;
    }

    .btn-export {
        margin-top: 2rem;
        padding: 0.5rem 1rem;
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }

}
</style>
