const API_BASE = '/api/ribs'

export async function getRibs() {
    const res = await fetch(API_BASE)
    if (!res.ok) throw new Error('Erreur lors du chargement des RIBs')
    return await res.json()
}

export async function getRibById(id) {
    const res = await fetch(`${API_BASE}/${id}`)
    if (!res.ok) throw new Error('Erreur lors du chargement du RIB')
    return await res.json()
}

export async function createRib(rib) {
    const res = await fetch('/api/ribs/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rib),
    });

    if (!res.ok) {
        let errorMessage = 'Erreur lors de la création du RIB';
        try {
            const errorData = await res.json();
            errorMessage = Object.values(errorData).flat().join(', ');
        } catch (e) {
            // Pas de corps JSON, on garde le message par défaut
        }
        throw new Error(errorMessage);
    }

    return await res.json();
}



export async function updateRib(id, rib) {
    const res = await fetch(`${API_BASE}/${id}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rib)
    })
    if (!res.ok) throw new Error('Erreur lors de la mise à jour du RIB')
    return await res.json()
}
export async function deleteRib(id) {
    const response = await fetch(`${API_BASE}/${id}/`, {
        method: 'DELETE',
    })
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Erreur lors de la suppression')
    }
    return true
}

