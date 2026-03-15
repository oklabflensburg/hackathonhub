/**
 * API Response Mapper Functions
 * 
 * Zentrale Mapper-Funktionen für die Transformation von API-Responses (snake_case)
 * zu Frontend-Typen (camelCase) und umgekehrt.
 * 
 * Diese Mapper stellen Konsistenz zwischen Backend-API und Frontend-Typen sicher.
 */

import type {
  Team,
  TeamMember,
  TeamInvitation,
  TeamCreateUpdatePayload
} from '~/types/team-types'
import {
  TeamRole,
  TeamStatus,
  TeamVisibility,
  TeamInvitationStatus
} from '~/types/team-types'

import type {
  Hackathon,
  Prize,
  Organizer,
  HackathonRegistration,
  HackathonRegistrationStatus,
  HackathonCreateData,
  HackathonUpdateData
} from '~/types/hackathon-types'
import {
  HackathonStatus
} from '~/types/hackathon-types'

import type {
  Project,
  ProjectTechnology,
  ProjectTag,
  ProjectTeamMember,
  ProjectStats
} from '~/types/project-types'
import {
  ProjectStatus,
  ProjectVisibility
} from '~/types/project-types'

import type {
  Comment
} from '~/types/comment-types'
import {
  CommentVoteType,
  CommentStatus
} from '~/types/comment-types'

import type {
  FileMetadata,
  ApiUploadResponse,
  ApiFileMetadata
} from '~/types/file-upload-types'
import {
  FileType,
  FileUploadStatus
} from '~/types/file-upload-types'

// ==================== HELPER FUNCTIONS ====================

/**
 * Konvertiert snake_case Objekt zu camelCase
 */
export function snakeToCamel<T extends Record<string, any>>(obj: T): any {
  if (Array.isArray(obj)) {
    return obj.map(snakeToCamel)
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc: any, key: string) => {
      const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
      acc[camelKey] = snakeToCamel(obj[key])
      return acc
    }, {})
  }
  return obj
}

/**
 * Konvertiert camelCase Objekt zu snake_case
 */
export function camelToSnake<T extends Record<string, any>>(obj: T): any {
  if (Array.isArray(obj)) {
    return obj.map(camelToSnake)
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc: any, key: string) => {
      const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
      acc[snakeKey] = camelToSnake(obj[key])
      return acc
    }, {})
  }
  return obj
}

/**
 * Konvertiert String-ID zu Number (für API-Payloads)
 */
export function idToNumber(id: string | number): number {
  if (typeof id === 'string') {
    const num = parseInt(id, 10)
    return isNaN(num) ? 0 : num
  }
  return id
}

/**
 * Konvertiert Number-ID zu String (für Frontend-Typen)
 */
export function idToString(id: string | number): string {
  if (typeof id === 'number') {
    return id.toString()
  }
  return id
}

// ==================== TEAM MAPPERS ====================

/**
 * API Team Response zu Frontend Team mappen
 */
export function mapApiTeamToTeam(apiTeam: any): Team {
  const team = snakeToCamel(apiTeam)
  
  return {
    id: idToString(team.id),
    name: team.name || '',
    description: team.description || null,
    slug: team.slug || team.name?.toLowerCase().replace(/\s+/g, '-') || '',
    avatarUrl: team.avatarUrl || null,
    bannerUrl: team.bannerUrl || null,
    visibility: team.isOpen ? TeamVisibility.PUBLIC : TeamVisibility.PRIVATE,
    status: team.status || TeamStatus.ACTIVE,
    maxMembers: team.maxMembers || null,
    createdAt: team.createdAt || new Date().toISOString(),
    updatedAt: team.updatedAt || team.createdAt || new Date().toISOString(),
    createdBy: idToString(team.createdBy),
    hackathonId: team.hackathonId ? idToString(team.hackathonId) : null,
    tags: team.tags || [],
    stats: {
      memberCount: team.memberCount || team._memberCount || 0,
      projectCount: team.projectCount || 0,
      activeProjectCount: team.activeProjectCount || 0,
      completedProjectCount: team.completedProjectCount || 0,
      totalVotes: team.totalVotes || 0,
      totalComments: team.totalComments || 0,
      averageRating: team.averageRating || null,
      lastActivityAt: team.lastActivityAt || null,
      viewCount: team.viewCount || 0,
      engagementScore: team.engagementScore || 0,
      engagementLevel: team.engagementLevel || 'low'
    }
  }
}

/**
 * Frontend Team zu API Team Payload mappen
 */
export function mapTeamToApiPayload(team: TeamCreateUpdatePayload & { id?: string }): any {
  const payload = camelToSnake(team)
  
  const result: any = {
    ...payload,
    hackathon_id: team.hackathonId ? idToNumber(team.hackathonId) : null,
    is_open: team.visibility === TeamVisibility.PUBLIC,
    max_members: team.maxMembers || null
  }
  
  // ID nur hinzufügen wenn vorhanden (für Updates)
  if (team.id) {
    result.id = idToNumber(team.id)
  }
  
  return result
}

/**
 * API Team Member zu Frontend Team Member mappen
 */
export function mapApiTeamMemberToTeamMember(apiMember: any): TeamMember {
  const member = snakeToCamel(apiMember)
  
  return {
    id: idToString(member.id),
    userId: idToString(member.userId),
    teamId: idToString(member.teamId),
    role: member.role as TeamRole,
    joinedAt: member.joinedAt || new Date().toISOString(),
    user: member.user ? {
      id: idToString(member.user.id),
      username: member.user.username || '',
      displayName: member.user.displayName || null,
      avatarUrl: member.user.avatarUrl || null,
      email: member.user.email || null,
      bio: member.user.bio || null,
      skills: member.user.skills || []
    } : undefined
  }
}

// ==================== HACKATHON MAPPERS ====================

/**
 * API Hackathon Response zu Frontend Hackathon mappen
 */
export function mapApiHackathonToHackathon(apiHackathon: any): Hackathon {
  const hackathon = snakeToCamel(apiHackathon)
  
  // Status mapping
  let status: HackathonStatus
  switch (hackathon.status) {
    case 'upcoming':
    case 'active':
    case 'completed':
    case 'draft':
    case 'cancelled':
      status = hackathon.status as HackathonStatus
      break
    default:
      status = HackathonStatus.UPCOMING
  }
  
  return {
    id: idToString(hackathon.id),
    name: hackathon.name || '',
    description: hackathon.description || '',
    shortDescription: hackathon.shortDescription || null,
    startDate: hackathon.startDate || hackathon.start_date || '',
    endDate: hackathon.endDate || hackathon.end_date || '',
    location: hackathon.location || '',
    imageUrl: hackathon.imageUrl || hackathon.image_url || null,
    bannerUrl: hackathon.bannerUrl || null,
    status,
    isActive: hackathon.isActive || hackathon.is_active || false,
    participantCount: hackathon.participantCount || hackathon.participant_count || 0,
    viewCount: hackathon.viewCount || hackathon.view_count || 0,
    projectCount: hackathon.projectCount || hackathon.project_count || 0,
    registrationDeadline: hackathon.registrationDeadline || hackathon.registration_deadline || null,
    prizes: hackathon.prizes || [],
    rules: hackathon.rules || '',
    organizers: hackathon.organizers || [],
    prizePool: hackathon.prizePool || hackathon.prize_pool || null,
    createdAt: hackathon.createdAt || hackathon.created_at || new Date().toISOString(),
    updatedAt: hackathon.updatedAt || hackathon.updated_at || new Date().toISOString(),
    tags: hackathon.tags || [],
    websiteUrl: hackathon.websiteUrl || null,
    contactEmail: hackathon.contactEmail || null,
    maxParticipants: hackathon.maxParticipants || null,
    isVirtual: hackathon.isVirtual || hackathon.is_virtual || false,
    timezone: hackathon.timezone || null,
    slug: hackathon.slug,
    stats: hackathon.stats ? {
      teamCount: hackathon.stats.teamCount || 0,
      projectCount: hackathon.stats.projectCount || 0,
      participantCount: hackathon.stats.participantCount || 0,
      averageTeamSize: hackathon.stats.averageTeamSize || 0,
      prizeCount: hackathon.stats.prizeCount || 0,
      submissionCount: hackathon.stats.submissionCount || 0,
      lastActivityAt: hackathon.stats.lastActivityAt || null
    } : undefined
  }
}

/**
 * API Hackathon Registration zu Frontend Hackathon Registration mappen
 */
export function mapApiHackathonRegistrationToHackathonRegistration(apiRegistration: any): HackathonRegistration {
  const registration = snakeToCamel(apiRegistration)
  
  return {
    id: idToString(registration.id),
    userId: idToString(registration.userId),
    hackathonId: idToString(registration.hackathonId),
    status: registration.status || 'pending',
    registeredAt: registration.registeredAt || registration.registered_at || new Date().toISOString(),
    user: registration.user ? snakeToCamel(registration.user) : undefined,
    hackathon: registration.hackathon ? snakeToCamel(registration.hackathon) : undefined
  }
}

/**
 * API Hackathon Registration Status zu Frontend mappen
 */
export function mapApiHackathonRegistrationStatusToHackathonRegistrationStatus(apiStatus: any): HackathonRegistrationStatus {
  const status = snakeToCamel(apiStatus)
  
  return {
    isRegistered: status.isRegistered || status.is_registered || false,
    hackathonId: idToString(status.hackathonId || status.hackathon_id),
    userId: status.userId ? idToString(status.userId) : undefined,
    registrationId: status.registrationId ? idToString(status.registrationId) : undefined,
    status: status.status || 'pending',
    registeredAt: status.registeredAt || status.registered_at || undefined
  }
}

/**
 * Frontend Hackathon Create/Update Data zu API Payload mappen
 */
export function mapHackathonCreateUpdateDataToApi(data: HackathonCreateData | HackathonUpdateData): any {
  const payload = camelToSnake(data)
  
  // ID Konvertierung falls vorhanden
  const result: any = { ...payload }
  
  // Spezielle Feld-Konvertierungen
  if ('startDate' in data && data.startDate) {
    result.start_date = data.startDate
  }
  if ('endDate' in data && data.endDate) {
    result.end_date = data.endDate
  }
  if ('imageUrl' in data) {
    result.image_url = data.imageUrl
  }
  if ('maxParticipants' in data) {
    result.max_participants = data.maxParticipants
  }
  if ('registrationOpen' in data) {
    result.registration_open = data.registrationOpen
  }
  if ('prizePool' in data) {
    result.prize_pool = data.prizePool
  }
  
  return result
}

// ==================== PROJECT MAPPERS ====================

/**
 * API Project Response zu Frontend Project mappen
 */
export function mapApiProjectToProject(apiProject: any): Project {
  const project = snakeToCamel(apiProject)
  const imagePath = project.imagePath || project.featuredImage || null
  
  // Status mapping
  let status: ProjectStatus
  switch (project.status) {
    case 'draft':
    case 'active':
    case 'completed':
    case 'archived':
    case 'under_review':
      status = project.status as ProjectStatus
      break
    default:
      status = ProjectStatus.DRAFT
  }
  
  // Visibility mapping
  let visibility: ProjectVisibility
  switch (project.visibility) {
    case 'public':
    case 'private':
    case 'team_only':
      visibility = project.visibility as ProjectVisibility
      break
    default:
      visibility = ProjectVisibility.PUBLIC
  }
  
  return {
    id: idToString(project.id),
    title: project.title || '',
    slug: project.slug || project.title?.toLowerCase().replace(/\s+/g, '-') || '',
    description: project.description || '',
    shortDescription: project.shortDescription || '',
    content: project.content || '',
    status,
    visibility,
    featuredImage: project.featuredImage || imagePath,
    imagePath,
    galleryImages: project.galleryImages || [],
    createdAt: project.createdAt || project.created_at || new Date().toISOString(),
    updatedAt: project.updatedAt || project.updated_at || new Date().toISOString(),
    publishedAt: project.publishedAt || null,
    deadline: project.deadline || null,
    team: project.team || [],
    technologies: project.technologies || [],
    tags: project.tags || [],
    hackathonId: project.hackathonId ? idToString(project.hackathonId) : undefined,
    hackathonName: project.hackathonName || '',
    stats: {
      views: project.stats?.views || 0,
      votes: project.stats?.votes || 0,
      comments: project.stats?.comments || 0,
      shares: project.stats?.shares || 0,
      bookmarks: project.stats?.bookmarks || 0
    },
    userVote: project.userVote || null,
    isBookmarked: project.isBookmarked || false,
    isFollowing: project.isFollowing || false,
    metaTitle: project.metaTitle || '',
    metaDescription: project.metaDescription || '',
    keywords: project.keywords || []
  }
}

// ==================== COMMENT MAPPERS ====================

/**
 * API Comment Response zu Frontend Comment mappen
 */
export function mapApiCommentToComment(apiComment: any): Comment {
  const comment = snakeToCamel(apiComment)
  
  // Vote type mapping
  let userVote: CommentVoteType
  switch (comment.userVote) {
    case 1:
      userVote = CommentVoteType.UPVOTE
      break
    case -1:
      userVote = CommentVoteType.DOWNVOTE
      break
    default:
      userVote = CommentVoteType.NONE
  }
  
  // Status mapping
  let status: CommentStatus
  switch (comment.status) {
    case 'active':
    case 'deleted':
    case 'hidden':
    case 'flagged':
      status = comment.status as CommentStatus
      break
    default:
      status = CommentStatus.ACTIVE
  }
  
  return {
    id: idToString(comment.id),
    content: comment.content || '',
    userId: idToString(comment.userId),
    userName: comment.userName || '',
    userAvatarUrl: comment.userAvatarUrl || null,
    userRole: comment.userRole || null,
    parentId: comment.parentId ? idToString(comment.parentId) : null,
    entityType: comment.entityType || 'project',
    entityId: idToString(comment.entityId),
    voteCount: comment.voteCount || 0,
    userVote,
    replyCount: comment.replyCount || 0,
    status,
    createdAt: comment.createdAt || comment.created_at || new Date().toISOString(),
    updatedAt: comment.updatedAt || comment.updated_at || new Date().toISOString(),
    deletedAt: comment.deletedAt || null,
    replies: comment.replies ? comment.replies.map(mapApiCommentToComment) : [],
    isEdited: comment.isEdited || false,
    metadata: comment.metadata || {}
  }
}

// ==================== GENERIC MAPPERS ====================

/**
 * Generischer Mapper für Paginated API Responses
 */
export function mapPaginatedResponse<T>(
  apiResponse: any,
  itemMapper: (item: any) => T
): {
  items: T[]
  totalCount: number
  page: number
  pageSize: number
  totalPages: number
} {
  const response = snakeToCamel(apiResponse)
  
  return {
    items: Array.isArray(response.items) ? response.items.map(itemMapper) : [],
    totalCount: response.totalCount || response.total_count || 0,
    page: response.page || 1,
    pageSize: response.pageSize || response.page_size || 20,
    totalPages: response.totalPages || response.total_pages || 1
  }
}

/**
 * Mapper für Error Responses
 */
export function mapApiError(error: any): {
  message: string
  code?: string
  details?: Record<string, any>
} {
  if (error.response?.data) {
    const data = snakeToCamel(error.response.data)
    return {
      message: data.message || error.message || 'Unknown error',
      code: data.code,
      details: data.details
    }
  }
  
  return {
    message: error.message || 'Unknown error'
  }
}

// ==================== FILE UPLOAD MAPPERS ====================

/**
 * API Upload Response zu Frontend FileMetadata mappen
 */
export function mapApiUploadResponseToFileMetadata(apiResponse: ApiUploadResponse): FileMetadata {
  // Extrahiere Dateiname aus file_path
  const filePath = apiResponse.file_path || ''
  const fileName = apiResponse.filename || filePath.split('/').pop() || 'unknown'
  const fileExtension = fileName.includes('.') ? fileName.split('.').pop()?.toLowerCase() || '' : ''
  
  // Bestimme FileType basierend auf MIME-Type oder Extension
  let fileType: FileType = FileType.OTHER
  if (fileExtension.match(/^(jpg|jpeg|png|gif|webp|svg)$/)) {
    fileType = FileType.IMAGE
  } else if (fileExtension.match(/^(pdf|doc|docx|txt|rtf)$/)) {
    fileType = FileType.DOCUMENT
  } else if (fileExtension.match(/^(mp4|webm|ogg|mov)$/)) {
    fileType = FileType.VIDEO
  } else if (fileExtension.match(/^(mp3|wav|ogg|webm)$/)) {
    fileType = FileType.AUDIO
  } else if (fileExtension.match(/^(zip|rar|tar|gz)$/)) {
    fileType = FileType.ARCHIVE
  }
  
  // Bestimme MIME-Type basierend auf Extension
  const mimeTypeMap: Record<string, string> = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'webp': 'image/webp',
    'svg': 'image/svg+xml',
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'rtf': 'application/rtf',
    'mp4': 'video/mp4',
    'mp3': 'audio/mpeg'
  }
  
  const mimeType = mimeTypeMap[fileExtension] || 'application/octet-stream'
  
  return {
    id: `file_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    name: fileName,
    size: 0, // Größe nicht in API-Response verfügbar
    type: fileType,
    mimeType,
    extension: fileExtension ? `.${fileExtension}` : '',
    url: apiResponse.url || '',
    thumbnailUrl: null,
    dimensions: undefined,
    duration: undefined,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    uploadedBy: '', // Wird vom Backend gesetzt
    entityType: 'project', // Standardwert, sollte vom Uploader gesetzt werden
    entityId: '',
    tags: [],
    description: null,
    isPublic: true,
    metadata: {}
  }
}

/**
 * API File Metadata zu Frontend FileMetadata mappen
 */
export function mapApiFileMetadataToFileMetadata(apiFile: ApiFileMetadata): FileMetadata {
  // FileType mapping
  let fileType: FileType = FileType.OTHER
  switch (apiFile.type) {
    case 'image':
      fileType = FileType.IMAGE
      break
    case 'document':
      fileType = FileType.DOCUMENT
      break
    case 'video':
      fileType = FileType.VIDEO
      break
    case 'audio':
      fileType = FileType.AUDIO
      break
    case 'archive':
      fileType = FileType.ARCHIVE
      break
    default:
      fileType = FileType.OTHER
  }
  
  return {
    id: apiFile.id,
    name: apiFile.name,
    size: apiFile.size,
    type: fileType,
    mimeType: apiFile.mime_type,
    extension: apiFile.extension,
    url: apiFile.url,
    thumbnailUrl: apiFile.thumbnail_url || null,
    dimensions: apiFile.dimensions,
    duration: apiFile.duration,
    createdAt: apiFile.created_at,
    updatedAt: apiFile.updated_at,
    uploadedBy: apiFile.uploaded_by,
    entityType: apiFile.entity_type,
    entityId: apiFile.entity_id,
    tags: apiFile.tags,
    description: apiFile.description || null,
    isPublic: apiFile.is_public,
    metadata: apiFile.metadata || {}
  }
}

/**
 * Frontend FileMetadata zu API FileMetadata mappen
 */
export function mapFileMetadataToApiFileMetadata(file: FileMetadata): ApiFileMetadata {
  // FileType mapping zurück zu string
  let fileTypeString = 'other'
  switch (file.type) {
    case FileType.IMAGE:
      fileTypeString = 'image'
      break
    case FileType.DOCUMENT:
      fileTypeString = 'document'
      break
    case FileType.VIDEO:
      fileTypeString = 'video'
      break
    case FileType.AUDIO:
      fileTypeString = 'audio'
      break
    case FileType.ARCHIVE:
      fileTypeString = 'archive'
      break
    default:
      fileTypeString = 'other'
  }
  
  return {
    id: file.id,
    name: file.name,
    size: file.size,
    type: fileTypeString,
    mime_type: file.mimeType,
    extension: file.extension,
    url: file.url,
    thumbnail_url: file.thumbnailUrl || null,
    dimensions: file.dimensions,
    duration: file.duration,
    created_at: file.createdAt,
    updated_at: file.updatedAt,
    uploaded_by: file.uploadedBy,
    entity_type: file.entityType,
    entity_id: file.entityId,
    tags: file.tags,
    description: file.description || null,
    is_public: file.isPublic,
    metadata: file.metadata || {}
  }
}

// ==================== EXPORT ALL MAPPERS ====================

export const apiMappers = {
  // Helper functions
  snakeToCamel,
  camelToSnake,
  idToNumber,
  idToString,
  
  // Team mappers
  mapApiTeamToTeam,
  mapTeamToApiPayload,
  mapApiTeamMemberToTeamMember,
  
  // Hackathon mappers
  mapApiHackathonToHackathon,
  mapApiHackathonRegistrationToHackathonRegistration,
  mapApiHackathonRegistrationStatusToHackathonRegistrationStatus,
  mapHackathonCreateUpdateDataToApi,
  
  // Project mappers
  mapApiProjectToProject,
  
  // Comment mappers
  mapApiCommentToComment,
  
  // File upload mappers
  mapApiUploadResponseToFileMetadata,
  mapApiFileMetadataToFileMetadata,
  mapFileMetadataToApiFileMetadata,
  
  // Generic mappers
  mapPaginatedResponse,
  mapApiError
}

export default apiMappers
