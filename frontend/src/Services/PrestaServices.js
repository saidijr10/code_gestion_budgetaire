

const API_BASE = '/api/prestataires/' // Grâce à vue.config.js avec proxy

export async function createPrestataire(data) {
    const response = await fetch(API_BASE, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

    const result = await response.json()

    if (!response.ok) {
        throw result
    }

    return result
}

export async function getPrestataires() {
    const response = await fetch(API_BASE)
    const data = await response.json()

    if (!response.ok) {
        throw data
    }

    return data
}

export async function deletePrestataire(id) {
    const response = await fetch(`${API_BASE}${id}/`, {
        method: 'DELETE',
    })
    if (!response.ok) {
        const err = await response.json()
        throw err
    }
    return true
}

export async function getPrestataireById(id) {
    const response = await fetch(`/api/prestataires/${id}/`)
    const data = await response.json()
    if (!response.ok) throw data
    return data
}

export async function updatePrestataire(id, payload) {
    const response = await fetch(`/api/prestataires/${id}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    })
    const data = await response.json()
    if (!response.ok) throw data
    return data
}

