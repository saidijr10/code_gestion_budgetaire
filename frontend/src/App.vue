<template>
  <nav class="app-nav">
    <div class="nav-container">


      <!-- Menu principal -->
      <div class="nav-menu">
        <!-- Lien vers la page d'accueil -->
          <div class="nav-item">
            <router-link to="/" exact-active-class="dropdown-link-active" class="nav-button">
              Accueil
            </router-link>
          </div>

        <!-- Gestion Prestataire -->
        <div class="nav-item" @mouseenter="showDropdown('prestataire')" @mouseleave="hideDropdown('prestataire')">
          <button class="nav-button" @click="toggleDropdown('prestataire')">
            Gestion Prestataire
            <svg class="dropdown-icon" :class="{ 'rotate': activeDropdown === 'prestataire' }" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd" />
            </svg>
          </button>
          <div class="dropdown-menu" :class="{ 'show': activeDropdown === 'prestataire' }">
            <router-link to="/ajout-pres" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fill-rule="evenodd"
                  d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                  clip-rule="evenodd" />
              </svg>
              Ajouter prestataire
            </router-link>
            <router-link to="/liste" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clip-rule="evenodd" />
              </svg>
              Liste prestataires
            </router-link>
          </div>
        </div>

        <!-- Gestion RIB -->
        <div class="nav-item" @mouseenter="showDropdown('rib')" @mouseleave="hideDropdown('rib')">
          <button class="nav-button" @click="toggleDropdown('rib')">
            Gestion RIB
            <svg class="dropdown-icon" :class="{ 'rotate': activeDropdown === 'rib' }" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd" />
            </svg>
          </button>
          <div class="dropdown-menu" :class="{ 'show': activeDropdown === 'rib' }">
            <router-link to="/ribs/add" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd" />
              </svg>
              Ajouter RIB
            </router-link>
            <router-link to="/ribs" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clip-rule="evenodd" />
              </svg>
              Liste RIB
            </router-link>
          </div>
        </div>

        <!-- Gestion Budget -->
        <div class="nav-item" @mouseenter="showDropdown('budget')" @mouseleave="hideDropdown('budget')">
          <button class="nav-button" @click="toggleDropdown('budget')">
            Gestion Budget
            <svg class="dropdown-icon" :class="{ 'rotate': activeDropdown === 'budget' }" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd" />
            </svg>
          </button>
          <div class="dropdown-menu" :class="{ 'show': activeDropdown === 'budget' }">
            <router-link to="/ajouter-budget" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd" />
              </svg>
              Ajouter Budget
            </router-link>
            <router-link to="/budgets" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clip-rule="evenodd" />
              </svg>
              Liste Budgets
            </router-link>
            <router-link to="/LigneBudgetaire/add" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd" />
              </svg>
              Ajouter Ligne Budget
            </router-link>
            <router-link to="/LigneBudgetaire" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clip-rule="evenodd" />
              </svg>
              Liste Lignes Budgétaires
            </router-link>
          </div>
        </div>

        <!-- Gestion Ordonnancements -->
        <div class="nav-item" @mouseenter="showDropdown('ordonnancement')" @mouseleave="hideDropdown('ordonnancement')">
          <button class="nav-button" @click="toggleDropdown('ordonnancement')">
            Gestion Ordonnancements
            <svg class="dropdown-icon" :class="{ 'rotate': activeDropdown === 'ordonnancement' }" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd" />
            </svg>
          </button>
          <div class="dropdown-menu" :class="{ 'show': activeDropdown === 'ordonnancement' }">
            <router-link to="/ordonnancements/ajouter" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd" />
              </svg>
              Ajouter Ordonnancement
            </router-link>
            <router-link to="/ordonnancements" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clip-rule="evenodd" />
              </svg>
              Liste Ordonnancements
            </router-link>
          </div>
        </div>

        <!-- Gestion Reglements -->
        <div class="nav-item" @mouseenter="showDropdown('reglement')" @mouseleave="hideDropdown('reglement')">
          <button class="nav-button" @click="toggleDropdown('reglement')">
            Gestion Règlements
            <svg class="dropdown-icon" :class="{ 'rotate': activeDropdown === 'reglement' }" viewBox="0 0 20 20"
              fill="currentColor">
              <path fill-rule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clip-rule="evenodd" />
            </svg>
          </button>
          <div class="dropdown-menu" :class="{ 'show': activeDropdown === 'reglement' }">
            <router-link to="/reglements/ajouter" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clip-rule="evenodd" />
              </svg>
              Ajouter Règlement
            </router-link>
            <router-link to="/reglements" exact-active-class="dropdown-link-active" class="dropdown-link">
              <svg class="link-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd"
                  d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                  clip-rule="evenodd" />
              </svg>
              Liste Règlements
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <router-view />
</template>

<script setup>
import { ref } from 'vue'

const activeDropdown = ref(null)

const showDropdown = (dropdown) => {
  activeDropdown.value = dropdown
}

const hideDropdown = (dropdown) => {
  if (activeDropdown.value === dropdown) {
    setTimeout(() => {
      activeDropdown.value = null
    }, 200) // Petit délai pour permettre la navigation
  }
}

const toggleDropdown = (dropdown) => {
  if (activeDropdown.value === dropdown) {
    activeDropdown.value = null
  } else {
    activeDropdown.value = dropdown
  }
}
</script>

<style scoped>
.app-nav {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  margin-bottom: 2rem;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
}

.nav-brand h2 {
  color: white;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-item {
  position: relative;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: white;
  padding: 1rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  transform: translateY(-1px);
}

.dropdown-icon {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s ease;
}

.dropdown-icon.rotate {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  min-width: 250px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  border-bottom: 1px solid #f3f4f6;
}

.dropdown-link:last-child {
  border-bottom: none;
}

.dropdown-link:hover {
  background: linear-gradient(135deg, #f8faff 0%, #e8f2ff 100%);
  color: #2563eb;
  padding-left: 1.5rem;
}

.dropdown-link-active {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
}

.dropdown-link-active:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  color: white;
  padding-left: 1.25rem;
}

.link-icon {
  width: 1.125rem;
  height: 1.125rem;
  flex-shrink: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-button {
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
  }

  .dropdown-menu {
    min-width: 200px;
  }
}

@media (max-width: 480px) {
  .nav-menu {
    flex-direction: column;
    width: 100%;
  }

  .nav-item {
    width: 100%;
  }

  .nav-button {
    width: 100%;
    justify-content: center;
  }

  .dropdown-menu {
    position: static;
    width: 100%;
    margin-top: 0.5rem;
    box-shadow: none;
    border: 1px solid #e5e7eb;
  }
}
</style>