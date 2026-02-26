export function resolveImageUrl(imagePath: string | null | undefined, backendUrl?: string): string {
  if (!imagePath) return ''

  const raw = imagePath.trim()
  if (!raw) return ''

  if (
    raw.startsWith('http://') ||
    raw.startsWith('https://') ||
    raw.startsWith('data:') ||
    raw.startsWith('blob:')
  ) {
    return raw
  }

  const base = (backendUrl || '').replace(/\/$/, '')

  if (raw.startsWith('/static/')) return `${base}${raw}`
  if (raw.startsWith('/uploads/')) return `${base}/static${raw}`
  if (raw.startsWith('uploads/')) return `${base}/static/${raw}`

  const normalized = raw.startsWith('/') ? raw.slice(1) : raw

  if (
    normalized.startsWith('projects/') ||
    normalized.startsWith('hackathons/') ||
    normalized.startsWith('avatars/')
  ) {
    return `${base}/static/uploads/${normalized}`
  }

  if (raw.startsWith('/')) return `${base}${raw}`
  return `${base}/${raw}`
}

export function normalizeUploadPathForApi(imagePath: string | null | undefined): string | null {
  if (!imagePath) return null

  const raw = imagePath.trim()
  if (!raw) return null

  if (raw.startsWith('http://') || raw.startsWith('https://')) {
    const parsed = new URL(raw)
    return normalizeUploadPathForApi(parsed.pathname)
  }

  if (raw.startsWith('/static/uploads/')) return raw
  if (raw.startsWith('static/uploads/')) return `/${raw}`
  if (raw.startsWith('/uploads/')) return `/static${raw}`
  if (raw.startsWith('uploads/')) return `/static/${raw}`

  const normalized = raw.startsWith('/') ? raw.slice(1) : raw
  if (
    normalized.startsWith('projects/') ||
    normalized.startsWith('hackathons/') ||
    normalized.startsWith('avatars/')
  ) {
    return `/static/uploads/${normalized}`
  }

  return raw.startsWith('/') ? raw : `/${raw}`
}
