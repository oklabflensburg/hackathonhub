/**
 * Utility functions for generating placeholder images
 */

/**
 * Generate a simple SVG placeholder image with a colored background and text
 * @param id - Unique identifier for consistent color selection
 * @param text - Text to display (usually first letter or initials)
 * @param width - Image width in pixels (default: 800)
 * @param height - Image height in pixels (default: 400)
 * @returns Data URL for the SVG image
 */
export function generatePlaceholderImage(
  id: number | string,
  text: string,
  width: number = 800,
  height: number = 400
): string {
  // Simple color palette based on ID
  const colors = [
    '#667eea', // Indigo
    '#f093fb', // Pink
    '#4facfe', // Blue
    '#43e97b', // Green
    '#fa709a', // Rose
    '#a8edea', // Cyan
    '#f6d365', // Yellow
    '#fda085', // Orange
    '#96e6a1', // Light Green
    '#d4fc79', // Lime
  ]
  
  // Convert id to number for consistent color selection
  const idNum = typeof id === 'string' ? 
    id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) : 
    id
  
  const color = colors[Math.abs(idNum) % colors.length] || '#667eea'
  
  // Get first letter or first two characters
  const displayText = text.trim().length > 0 ? 
    text.trim().charAt(0).toUpperCase() : 
    '?'
  
  // Calculate font size based on container size
  const fontSize = Math.min(width, height) * 0.3
  
  // Simple SVG
  const svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="${color}" />
    <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="${fontSize}" 
          font-weight="bold" fill="white" text-anchor="middle" dy="0.35em" 
          opacity="0.9">${displayText}</text>
  </svg>`
  
  return 'data:image/svg+xml;base64,' + btoa(svg)
}

/**
 * Generate a placeholder image for a project
 * @param project - Project object with id and title/name
 * @param width - Image width (default: 800)
 * @param height - Image height (default: 400)
 * @returns Data URL for the placeholder image
 */
export function generateProjectPlaceholder(
  project: { id: number | string; title?: string; name?: string },
  width: number = 800,
  height: number = 400
): string {
  const text = project.title || project.name || 'Project'
  return generatePlaceholderImage(project.id, text, width, height)
}

/**
 * Generate a placeholder image for a hackathon
 * @param hackathon - Hackathon object with id and name
 * @param width - Image width (default: 800)
 * @param height - Image height (default: 400)
 * @returns Data URL for the placeholder image
 */
export function generateHackathonPlaceholder(
  hackathon: { id: number | string; name?: string },
  width: number = 800,
  height: number = 400
): string {
  const text = hackathon.name || 'Hackathon'
  return generatePlaceholderImage(hackathon.id, text, width, height)
}

/**
 * Generate a placeholder image for a user/avatar
 * @param user - User object with id and username/name
 * @param size - Image size (width and height, default: 100)
 * @returns Data URL for the placeholder avatar
 */
export function generateAvatarPlaceholder(
  user: { id: number | string; username?: string; name?: string },
  size: number = 100
): string {
  const text = user.username || user.name || 'User'
  return generatePlaceholderImage(user.id, text, size, size)
}

/**
 * Get a fallback image URL for when no image is available
 * This is a simpler alternative to SVG generation
 * @param type - Type of placeholder ('project', 'hackathon', 'avatar', 'generic')
 * @returns URL string
 */
export function getFallbackImageUrl(type: 'project' | 'hackathon' | 'avatar' | 'generic' = 'generic'): string {
  // For now, we'll use SVG generation, but this could be extended to use
  // external placeholder services if needed
  switch (type) {
    case 'project':
      return generatePlaceholderImage(0, 'P', 800, 400)
    case 'hackathon':
      return generatePlaceholderImage(0, 'H', 800, 400)
    case 'avatar':
      return generatePlaceholderImage(0, 'U', 100, 100)
    default:
      return generatePlaceholderImage(0, '?', 800, 400)
  }
}